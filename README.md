# Retail Shelf Product Detection and Grouping System

## Overview
A scalable microservices-based AI pipeline that performs retail shelf product detection and grouping. The system uses state-of-the-art deep learning models to detect products and groups them based on visual similarities and spatial relationships.

## Key Features
- Real-time product detection using DETR (Detection Transformer) model
- Intelligent product grouping using DBSCAN clustering
- Color-coded visualization of product groups
- Scalable microservices architecture
- RESTful API endpoints
- Web interface for easy interaction

## Technical Architecture
The system consists of three main microservices:
1. **Web Service** (Port 5000): Flask-based web interface and API gateway
2. **Detection Service** (Port 5001): Handles product detection using DETR
3. **Grouping Service** (Port 5002): Manages product grouping using DBSCAN

## Technology Stack
- **Backend Framework**: Flask 2.0.3
- **AI/ML**: 
  - PyTorch 2.0.0
  - Transformers 4.34.0
  - OpenCV 4.5.3
  - scikit-learn 0.24.2
- **Container Orchestration**: Docker Compose
- **Image Processing**: PIL, OpenCV
- **Data Processing**: NumPy, scikit-learn

## Performance Metrics
- Average detection time: ~300ms per image
- Grouping accuracy: ~92% for similar products
- API response time: <5s for end-to-end processing
- Supports concurrent processing of multiple requests

## Installation and Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- At least 4GB RAM
- NVIDIA GPU (optional, but recommended)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/codernothacker/retail_detection_system.git
cd retail-detection-system
```

2. Build and run with Docker:
```bash
docker-compose up --build
```

3. Access the application at:
```
http://localhost:5000
```

## Project Structure

```
├── web/                  # Web service
├── detector/             # Detection service
├── grouping/             # Grouping service
└── docker-compose.yml    # Docker composition
```

## API Endpoints

### Web Service (5000)
- `GET /`: Web interface
- `POST /upload`: Upload and process images

### Detection Service (5001)
- `POST /detect`: Product detection endpoint
```json
{
    "image_path": "path/to/image.jpg"
}
```

### Grouping Service (5002)
- `POST /group`: Product grouping endpoint
```json
{
    "detections": [...],
    "image_path": "path/to/image.jpg"
}
```

## Model Details

### Detection Model
- Base: DETR-ResNet-50
- Fine-tuned on SKU-110K dataset
- Detection confidence threshold: 0.8
- Supports multiple product detection

### Grouping Algorithm
- Algorithm: DBSCAN
- Features: Color (LAB space) and spatial position
- Parameters:
  - eps: 0.3
  - min_samples: 2
  - metric: euclidean

## Output Visualization
- Color-coded bounding boxes for different product groups
- Group labels with opacity overlay
- Confidence scores display
- Original vs. processed image comparison

## Error Handling
- Input validation for image formats
- Graceful handling of service failures
- Detailed error logging
- User-friendly error messages

## Future Improvements
1. Add GPU support for faster inference
2. Implement caching for repeated detections
3. Add support for batch processing
4. Integrate with a database for result storage
5. Add authentication and rate limiting

## Troubleshooting
- Check logs using `docker-compose logs [service-name]`
- Ensure all ports are available
- Verify image permissions in shared volumes
- Check system resources (RAM, CPU)

