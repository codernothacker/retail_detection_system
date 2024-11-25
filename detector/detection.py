import torch
import cv2
import numpy as np
from PIL import Image, ImageOps
from transformers import DetrImageProcessor, DetrForObjectDetection

class ProductDetector:
    def __init__(self):
        print("Initializing ProductDetector...")
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
        self.model = DetrForObjectDetection.from_pretrained("isalia99/detr-resnet-50-sku110k").eval()
        print("ProductDetector initialized successfully")

    def detect(self, image_path):
        print(f"Processing image: {image_path}")
        try:

            image = Image.open(image_path)
            image = ImageOps.exif_transpose(image)

            inputs = self.processor(images=image, return_tensors="pt")
            outputs = self.model(**inputs)

            target_sizes = torch.tensor([image.size[::-1]])
            results = self.processor.post_process_object_detection(
                outputs, 
                target_sizes=target_sizes, 
                threshold=0.8
            )[0]

            detections = []
            for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                box = [round(i) for i in box.tolist()]
                detections.append({
                    'bbox': box,
                    'confidence': round(score.item(), 3),
                    'class': self.model.config.id2label[label.item()]
                })
            
            print(f"Found {len(detections)} detections")
            return detections
            
        except Exception as e:
            print(f"Error in detect method: {str(e)}")
            raise
