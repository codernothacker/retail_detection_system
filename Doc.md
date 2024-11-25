# Retail Product Detection System Documentation

# Retail Product Detection System Documentation

## Table of Contents
1. Project Overview
2. System Architecture
3. Installation & Setup
4. API Documentation
5. Technical Implementation
6. Code Organization
7. Alternative Approaches
8. Future Improvements

## 1. Project Overview

The Retail Product Detection System is a microservices-based application that detects and groups retail products in shelf images.

### Key Features
- Product detection using DETR (DEtection TRansformer) model
- Intelligent product grouping using DBSCAN clustering
- Color-coded visualization of product groups
- RESTful API architecture
- Docker containerization for easy deployment

### Example Results

#### Detection Output
![Detection Result](img\detector.jpg)

#### Grouped Products
![Grouped Products](img\group.jpg)

## Sample API Response

```json
{
    "status": "success",
    "detections": [
        {
            "bbox": [100, 200, 300, 400],
            "confidence": 0.95,
            "group": 1,
            "color": [255, 0, 0]
        }
    ]
}
```
## 2. System Architecture

### Microservices Architecture
```
├── web (Flask Frontend - Port 5000)
│   ├── static/uploads/    # Shared volume for images
│   ├── templates/         # HTML templates
│   └── app.py            # Web service
├── detector (Port 5001)
│   ├── app.py            # Detection service
│   └── detection.py      # DETR model implementation
└── grouping (Port 5002)
    ├── app.py            # Grouping service
    └── grouping.py       # DBSCAN clustering implementation
```

### Data Flow
1. Client uploads image → Web Service
2. Web Service → Detection Service (product detection)
3. Detection Service → Grouping Service (product grouping)
4. Grouped results → Web Service → Client

## 3. Installation & Setup

### Prerequisites
- Docker
- Docker Compose
- Git

### Setup Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd retail-detection-system
   ```

2. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   ```
   http://localhost:5000
   ```

## 4. API Documentation

### Web Service (Port 5000)

#### Upload Endpoint
- **URL**: `/upload`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `image`: Image file (jpg, jpeg, png)
- **Response**:
  ```json
  {
    "message": "Processing completed successfully",
    "original_image": "/static/uploads/image.jpg",
    "detected_image": "/static/uploads/detected_image.jpg",
    "detections": [
      {
        "bbox": [x1, y1, x2, y2],
        "confidence": 0.95,
        "group": 1,
        "color": [255, 0, 0]
      }
    ]
  }
  ```

### Detection Service (Port 5001)

#### Detect Endpoint
- **URL**: `/detect`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "image_path": "/app/images/image.jpg"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "detections": [
      {
        "bbox": [x1, y1, x2, y2],
        "confidence": 0.95,
        "class": "product"
      }
    ],
    "count": 10
  }
  ```

### Grouping Service (Port 5002)

#### Group Endpoint
- **URL**: `/group`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "detections": [...],
    "image_path": "/app/images/image.jpg"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "grouped_detections": [
      {
        "bbox": [x1, y1, x2, y2],
        "confidence": 0.95,
        "group": 1,
        "color": [255, 0, 0]
      }
    ]
  }
  ```

## 5. Technical Implementation

### Detection Service
- Uses DETR (DEtection TRansformer) model fine-tuned on SKU-110K dataset
- Model: `facebook/detr-resnet-50`
- Confidence threshold: 0.8
- Returns bounding boxes with confidence scores

### Grouping Service
- Uses DBSCAN clustering algorithm
- Features used for grouping:
  - LAB color space features (70% weight)
  - Vertical position/shelf level (30% weight)
- Parameters:
  - eps: 0.3
  - min_samples: 2
  - metric: euclidean

### Visualization
- Color-coded bounding boxes for different groups
- Semi-transparent overlays (50% opacity)
- Group labels with white text on colored background
- Predefined color palette for consistent visualization

## 6. Code Organization

### Project Structure
```
├── web/
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css     # Custom styles
│   │   ├── js/
│   │   │   └── main.js        # Frontend JavaScript
│   │   ├── img/              # Static images
│   │   └── uploads/          # Uploaded images
│   ├── templates/
│   │   ├── index.html
│   │   └── result.html
│   ├── utils/
│   │   └── __init__.py       # Utility functions
│   ├── app.py
│   ├── config.py
│   └── Dockerfile
├── detector/
│   ├── utils/
│   │   └── __init__.py       # Detection utilities
│   ├── app.py
│   ├── detection.py
│   ├── config.py
│   └── Dockerfile
├── grouping/
│   ├── utils/
│   │   └── __init__.py       # Grouping utilities
│   ├── app.py
│   ├── grouping.py
│   ├── config.py
│   └── Dockerfile
├── docker-compose.yml
├── .env                      # Environment variables
├── .gitignore
└── README.md
```

### Configuration Management
The project now uses a structured configuration system:

1. **Environment Variables** (.env):
   - Service URLs
   - Debug settings
   - Model paths
   - File size limits

2. **Service-specific Configs**:
   - Web Service: Upload settings, service URLs
   - Detector: Model parameters, confidence thresholds
   - Grouping: Clustering parameters, visualization settings

### Utility Functions

1. **Web Service Utilities**:
   - Logger setup
   - File type validation
   - Error handling decorators

2. **Detector Service Utilities**:
   - Image preparation
   - Detection format conversion
   - Model output processing

3. **Grouping Service Utilities**:
   - Feature extraction
   - Visualization helpers
   - ROI processing

### Frontend Assets

1. **CSS (styles.css)**:
   - Responsive layout
   - Image preview styling
   - Loading animations
   - Error message styling

2. **JavaScript (main.js)**:
   - Image preview
   - Form validation
   - AJAX upload handling
   - Error handling
   - Loading states

### Error Handling
The system now includes centralized error handling:
- Consistent error response format
- Detailed logging
- Frontend error display
- Error recovery mechanisms

[Previous sections 7-8 remain the same]

## Additional Notes

### Frontend Implementation
The web interface now provides:
- Real-time image preview
- Upload progress indication
- Validation feedback
- Responsive design
- Error messaging

### Configuration Management
Environment variables can be configured through:
1. `.env` file for development
2. Docker environment variables
3. Service-specific config files

### Logging
Structured logging is implemented across all services:
- Timestamp
- Service identification
- Log levels
- Error tracing

### Development Workflow
1. Configure environment variables in `.env`
2. Build containers: `docker-compose build`
3. Start services: `docker-compose up`
4. Access web interface: `http://localhost:5000`

### Troubleshooting
Common issues and solutions:
1. Image upload fails:
   - Check file size limits
   - Verify allowed extensions
   - Check storage permissions

2. Detection service errors:
   - Verify model path
   - Check GPU availability
   - Monitor memory usage

3. Grouping service issues:
   - Adjust clustering parameters
   - Check feature extraction
   - Verify image format