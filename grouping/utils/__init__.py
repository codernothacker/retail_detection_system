import cv2
import numpy as np
from .error_handlers import handle_errors
def extract_roi_features(image, bbox):
    x1, y1, x2, y2 = map(int, bbox)
    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return None
    lab_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)
    avg_color = np.mean(lab_roi.reshape(-1, 3), axis=0)
    center_y = (y1 + y2) / (2 * image.shape[0])
    
    return np.concatenate([avg_color, [center_y]])

def draw_group_visualization(image, detections, opacity=0.5):
    vis_image = image.copy()
    for det in detections:
        bbox = det['bbox']
        color = det.get('color', (0, 0, 0))
        group = det.get('group', -1)
        
        overlay = vis_image.copy()
        cv2.rectangle(overlay, 
                     (bbox[0], bbox[1]), 
                     (bbox[2], bbox[3]), 
                     color, 
                     -1)
        cv2.addWeighted(overlay, opacity, vis_image, 1 - opacity, 0, vis_image)
        
    return vis_image