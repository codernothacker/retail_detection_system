import torch
import numpy as np
from PIL import Image
from .error_handlers import handle_errors

def prepare_image(image_path):
    """Prepare image for model input."""
    image = Image.open(image_path)
    # Add any necessary preprocessing steps
    return image

def convert_detections(model_output, confidence_threshold=0.8):
    """Convert model output to detection format."""
    detections = []
    for score, label, box in zip(
        model_output["scores"],
        model_output["labels"],
        model_output["boxes"]
    ):
        if score < confidence_threshold:
            continue
            
        detections.append({
            'bbox': [int(i) for i in box.tolist()],
            'confidence': float(score),
            'class': label.item()
        })
    return detections