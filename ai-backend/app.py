"""
AI Backend Service
Performs object detection using YOLOv8n model
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from ultralytics import YOLO
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import json
import uuid
from pathlib import Path

app = FastAPI(title="AI Detection Service")

# Load YOLOv8 nano model (optimized for CPU)
model = YOLO('yolov8n.pt')

# Output directory for annotated images and JSON
OUTPUT_DIR = Path("/app/outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Perform object detection on uploaded image
    
    Returns:
        JSON with detected objects, confidence scores, bounding boxes,
        and paths to annotated image and JSON file
    """
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Run inference
        results = model(image, conf=0.25)
        
        # Parse results
        detections = []
        annotated_image = image.copy()
        draw = ImageDraw.Draw(annotated_image)
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Extract detection info
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                class_name = result.names[int(box.cls[0])]
                confidence = float(box.conf[0])
                
                detection = {
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2]
                }
                detections.append(detection)
                
                # Draw bounding box
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                
                # Draw label
                label = f"{class_name} {confidence:.2f}"
                draw.text((x1, y1 - 10), label, fill="red")
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        image_filename = f"detection_{unique_id}.jpg"
        json_filename = f"detection_{unique_id}.json"
        
        # Save annotated image
        image_path = OUTPUT_DIR / image_filename
        annotated_image.save(image_path)
        
        # Save JSON file
        json_path = OUTPUT_DIR / json_filename
        result_data = {
            "success": True,
            "count": len(detections),
            "detections": detections,
            "image_file": image_filename
        }
        with open(json_path, 'w') as f:
            json.dump(result_data, f, indent=2)
        
        return {
            "success": True,
            "count": len(detections),
            "detections": detections,
            "annotated_image": f"/outputs/{image_filename}",
            "json_file": f"/outputs/{json_filename}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/outputs/{filename}")
async def get_output_file(filename: str):
    """
    Retrieve saved output file (image or JSON)
    """
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)


@app.get("/health")
def health_check():
    """Service health check"""
    return {"status": "healthy", "model": "yolov8n"}
