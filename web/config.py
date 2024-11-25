import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    DETECTION_SERVICE_URL = os.getenv('DETECTION_SERVICE_URL', 'http://detector:5001')
    GROUPING_SERVICE_URL = os.getenv('GROUPING_SERVICE_URL', 'http://grouping:5002')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
