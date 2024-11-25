import os

class DetectorConfig:
    MODEL_PATH = os.getenv('MODEL_PATH', 'facebook/detr-resnet-50')
    CONFIDENCE_THRESHOLD = 0.8
    MAX_DETECTIONS = 100
    DEVICE = 'cuda' if os.getenv('USE_GPU', '0') == '1' else 'cpu'