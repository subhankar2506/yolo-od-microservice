# YOLOv8 Object Detection Microservice

A microservice architecture for object detection using YOLOv8n, run using CPU inference on MacBook Air.

## Architecture Overview

This system consists of two independently deployable services:

- **UI Backend**: FastAPI service that handles image uploads and user requests (Port 8000)
- **AI Backend**: FastAPI service that performs object detection using YOLOv8n (Port 8001)

The services communicate via REST API and are orchestrated using Docker Compose.

## Project Structure

```
yolo-od-microservice/
├── README.md
├── docker-compose.yml
├── test_detection.py
├── outputs/                    # Generated annotated images and JSON files
├── ui-backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── ai-backend/
    ├── app.py
    ├── requirements.txt
    └── Dockerfile
```

## Prerequisites

- Minimum 8GB RAM
- 5GB free disk space (for Docker images and model)

## Installation

### Step 1: Verify Docker Installation

Ensure Docker Desktop is installed and running:

```bash
docker --version
docker-compose --version
```

If Docker is not installed, download from: https://www.docker.com/products/docker-desktop/

### Step 2: Start Docker Desktop

```bash
open -a Docker
```

### Step 3: Navigate to Project Directory

```bash
cd yolo-od-microservice
```

### Step 4: Build and Start Services

```bash
docker-compose up --build
```

First run takes approximately 3-5 minutes to download dependencies and the YOLOv8n model (6.2MB).

## Usage

### Web Interface

Open your browser and navigate to:

```
http://localhost:8000
```

Upload an image using the web form to get detection results.

### API Endpoint

**Endpoint**: `POST /detect`

**Example using curl**:

```bash
curl -X POST "http://localhost:8000/detect" \
  -F "file=@/path/to/image.jpg"
```

**Response Example Format**:

```json
{
  "success": true,
  "count": 2,
  "detections": [
    {
      "class": "person",
      "confidence": 0.89,
      "bbox": [120, 45, 380, 620]
    },
    {
      "class": "dog",
      "confidence": 0.76,
      "bbox": [200, 300, 450, 580]
    }
  ],
  "annotated_image": "/outputs/detection_a1b2c3d4.jpg",
  "json_file": "/outputs/detection_a1b2c3d4.json"
}
```

**Bounding Box Format**: `[x1, y1, x2, y2]` where (x1, y1) is top-left corner and (x2, y2) is bottom-right corner.

### Output Files

The service automatically generates two files for each detection:

1. **Annotated Image**: Original image with red bounding boxes and labels showing detected objects
2. **JSON File**: Detection results saved in JSON format

Files are saved in the `outputs/` directory:

```bash
# View generated files
ls outputs/

# Open annotated image
open outputs/detection_a1b2c3d4.jpg

# View JSON file
cat outputs/detection_a1b2c3d4.json
```

You can also download files via HTTP:

```bash
curl http://localhost:8001/outputs/detection_a1b2c3d4.jpg -o result.jpg
curl http://localhost:8001/outputs/detection_a1b2c3d4.json -o result.json
```

### Python Testing Script

```bash
python test_detection.py /path/to/image.jpg
```

Output example:

```
Detection successful!
Objects found: 2

1. person
   Confidence: 0.89
   BBox: [120, 45, 380, 620]

2. dog
   Confidence: 0.76
   BBox: [200, 300, 450, 580]

Output Files:
  Annotated Image: http://localhost:8001/outputs/detection_def45678.jpg
  JSON File: http://localhost:8001/outputs/detection_def45678.json

  Local files saved in: ./outputs/
```

## Service Endpoints

### UI Backend (Port 8000)

- `GET /` - Web interface for image upload
- `POST /detect` - Upload image and get detection results
- `GET /health` - Service health check

### AI Backend (Port 8001)

- `POST /predict` - Perform object detection on image
- `GET /outputs/{filename}` - Download annotated image or JSON file
- `GET /health` - Model and service health check

## Health Checks

Verify services are running:

```bash
# UI Backend
curl http://localhost:8000/health

# AI Backend
curl http://localhost:8001/health
```

## Stopping Services

### Graceful Shutdown

Press `Ctrl+C` in the terminal where docker-compose is running.

### Force Stop

```bash
docker-compose down
```

### Remove All Containers and Networks

```bash
docker-compose down --volumes --remove-orphans
```

## Technical Specifications

### Model Details

- **Model**: YOLOv8n (nano variant)
- **Size**: 6.2MB
- **Classes**: 80 object classes (COCO dataset)
- **Confidence Threshold**: 0.25 (configurable in `ai-backend/app.py`)
- **Inference Device**: CPU
