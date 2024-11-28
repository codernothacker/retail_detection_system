# Retail Product Detection System

A microservices-based system for detecting and grouping retail products in shelf images using DETR and DBSCAN clustering.

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

## Services

- Web Service (Port 5000): Frontend and API gateway
- Detection Service (Port 5001): Product detection using DETR
- Grouping Service (Port 5002): Product grouping using DBSCAN

## Project Structure

```
├── web/                  # Web service
├── detector/             # Detection service
├── grouping/             # Grouping service
└── docker-compose.yml    # Docker composition
```

## Configuration

1. Copy `.env.example` to `.env`
2. Modify environment variables as needed

## API Documentation

See `docs/API.md` for detailed API documentation.
