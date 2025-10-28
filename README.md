# Object Detection Microservice

A production-ready microservice architecture for object detection using YOLOv8n, optimized for CPU inference on MacBook Air.

## Architecture Overview

This system consists of two independently deployable services:

- **UI Backend**: FastAPI service that handles image uploads and user requests (Port 8000)
- **AI Backend**: FastAPI service that performs object detection using YOLOv8n (Port 8001)

The services communicate via REST API and are orchestrated using Docker Compose.

## Project Structure

```
object-detection-microservice/
├── README.md
├── QUICKSTART.md
├── DEPLOYMENT.md
├── docker-compose.yml
├── test_detection.py
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

- Docker Desktop for Mac (version 20.x or higher)
- MacBook Air with M1/M2 or Intel processor
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

Wait for the Docker icon to appear in the menu bar and become steady (not animating).

### Step 3: Navigate to Project Directory

```bash
cd object-detection-microservice
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

**Response Format**:

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
  ]
}
```

**Bounding Box Format**: `[x1, y1, x2, y2]` where (x1, y1) is top-left corner and (x2, y2) is bottom-right corner.

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
```

## Service Endpoints

### UI Backend (Port 8000)

- `GET /` - Web interface for image upload
- `POST /detect` - Upload image and get detection results
- `GET /health` - Service health check

### AI Backend (Port 8001)

- `POST /predict` - Perform object detection on image
- `GET /health` - Model and service health check

## Health Checks

Verify services are running:

```bash
# UI Backend
curl http://localhost:8000/health

# AI Backend
curl http://localhost:8001/health
```

## API Documentation

Interactive API documentation is available when services are running:

- UI Backend: http://localhost:8000/docs
- AI Backend: http://localhost:8001/docs

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

### Performance Metrics

- **MacBook Air M1/M2**: 100-300ms per image
- **MacBook Air Intel**: 300-800ms per image
- **Memory Usage**: Approximately 1.5GB per AI backend container

### Detected Object Classes

person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, fire hydrant, stop sign, parking meter, bench, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush

## Configuration

### Adjusting Confidence Threshold

Edit `ai-backend/app.py`:

```python
results = model(image, conf=0.25)  # Change 0.25 to desired value
```

### Changing Ports

Edit `docker-compose.yml`:

```yaml
services:
  ui-backend:
    ports:
      - "8080:8000"  # Change 8080 to desired port
```

### Resource Limits

Edit `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
```

## Troubleshooting

### Docker daemon not running

```bash
open -a Docker
# Wait for Docker to start completely
```

### Port already in use

```bash
# Check what's using the port
lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

### Out of memory errors

Increase Docker memory allocation:
- Docker Desktop > Settings > Resources > Memory > 4GB or higher

### Slow inference times

- Ensure YOLOv8n model is being used (smallest variant)
- Check Docker resource allocation
- Monitor CPU usage: `docker stats`

### Model download fails

Pre-download the model:

```bash
docker-compose run ai-backend python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## Development

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f ai-backend
docker-compose logs -f ui-backend
```

### Rebuilding After Code Changes

```bash
docker-compose up --build
```

### Running Services Individually

```bash
# AI Backend only
docker-compose up ai-backend

# UI Backend only (requires AI Backend running)
docker-compose up ui-backend
```

## Support

For issues and questions:
- Check `DEPLOYMENT.md` for detailed troubleshooting
- Review `QUICKSTART.md` for quick setup guide
- Consult interactive API docs at `/docs` endpoints

## License

This project uses the following open-source components:
- YOLOv8 by Ultralytics (AGPL-3.0)
- FastAPI (MIT)
