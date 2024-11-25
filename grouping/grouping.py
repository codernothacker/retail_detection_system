import cv2
import numpy as np
from sklearn.cluster import DBSCAN
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ProductGrouper:
    def __init__(self):
        self.colors = {
            0: (0, 255, 0),     
            1: (255, 0, 0),     
            2: (0, 0, 255),    
            3: (255, 255, 0),  
            4: (255, 0, 255),  
            5: (0, 255, 255),   
            6: (255, 128, 0),   
            7: (128, 0, 255),   
            8: (0, 255, 128),   
            -1: (0, 0, 0)       
        }

    def extract_features(self, image, bbox):
        try:
            x1, y1, x2, y2 = map(int, bbox)
            h, w = image.shape[:2]
            roi = image[y1:y2, x1:x2]
            if roi.size == 0:
                return None
            roi = cv2.resize(roi, (64, 64))
            lab_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)
            avg_color = np.mean(lab_roi.reshape(-1, 3), axis=0)
            center_y = (y1 + y2) / (2 * h)
            features = np.concatenate([
                avg_color * 0.7, 
                [center_y * 0.3] 
            ])
            
            return features
            
        except Exception as e:
            logger.error(f"Feature extraction error: {str(e)}")
            return None

    def group_products(self, image, detections):
        try:
            if not detections:
                return []
            features = []
            valid_detections = []
            
            for det in detections:
                feature = self.extract_features(image, det['bbox'])
                if feature is not None:
                    features.append(feature)
                    valid_detections.append(det)
            
            if not features:
                return detections
            features = np.array(features)
            feature_mean = np.mean(features, axis=0)
            feature_std = np.std(features, axis=0) + 1e-8
            normalized_features = (features - feature_mean) / feature_std
            clustering = DBSCAN(
                eps=0.3,
                min_samples=2,
                metric='euclidean'
            )
            
            labels = clustering.fit_predict(normalized_features)
            logger.info(f"Found {len(set(labels))} groups")
            for det, label in zip(valid_detections, labels):
                det['group'] = int(label)
                det['color'] = self.colors.get(int(label), self.colors[-1])
            
            return valid_detections
            
        except Exception as e:
            logger.error(f"Grouping error: {str(e)}")
            return detections

    def visualize_groups(self, image, detections, output_path):
        try:
            img_copy = image.copy()
            detections = sorted(detections, key=lambda x: x.get('group', -1))
            for det in detections:
                x1, y1, x2, y2 = map(int, det['bbox'])
                group = det.get('group', -1)
                color = self.colors.get(group, self.colors[-1])
                overlay = img_copy.copy()
                cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
                cv2.addWeighted(overlay, 0.5, img_copy, 0.5, 0, img_copy)  
                label = f"Group {group if group >= 0 else 'U'}" 
                font_scale = 0.6
                thickness = 2
                font = cv2.FONT_HERSHEY_SIMPLEX
                (text_width, text_height), _ = cv2.getTextSize(label, font, font_scale, thickness)
                cv2.rectangle(img_copy,
                            (x1, y1 - text_height - 5),
                            (x1 + text_width, y1),
                            color,
                            -1)
                cv2.putText(img_copy, 
                          label,
                          (x1, y1 - 5),
                          font,
                          font_scale,
                          (255, 255, 255), 
                          thickness)
            cv2.imwrite(output_path, img_copy)
            return img_copy
        except Exception as e:
            logger.error(f"Visualization error: {str(e)}")
            return image