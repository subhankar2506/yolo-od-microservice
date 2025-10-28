"""
AI Backend Service
Performs object detection using YOLOv8n model
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from ultralytics import YOLO
import numpy as np
from PIL import Image
import io

app = FastAPI(title="AI Detection Service")

# Load YOLOv8 nano model (optimized for CPU)
model = YOLO('yolov8n.pt')


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Perform object detection on uploaded image
    
    Returns:
        JSON with detected objects, confidence scores, and bounding boxes
    """
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Run inference
        results = model(image, conf=0.25)
        
        # Parse results
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                detection = {
                    "class": result.names[int(box.cls[0])],
                    "confidence": float(box.conf[0]),
                    "bbox": box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                }
                detections.append(detection)
        
        return {
            "success": True,
            "count": len(detections),
            "detections": detections
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """Service health check"""
    return {"status": "healthy", "model": "yolov8n"}
