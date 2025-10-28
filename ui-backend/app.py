"""
UI Backend Service
Handles user image uploads and coordinates with AI backend
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import os

app = FastAPI(title="UI Backend Service")

AI_BACKEND_URL = os.getenv("AI_BACKEND_URL", "http://ai-backend:8001")


@app.get("/", response_class=HTMLResponse)
def home():
    """Simple UI for testing"""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Object Detection</title>
            <style>
                body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
                .result { margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 5px; }
                img { max-width: 100%; margin-top: 10px; }
                .download-links { margin-top: 15px; }
                .download-links a { margin-right: 15px; }
            </style>
        </head>
        <body>
            <h2>Object Detection Service</h2>
            <form action="/detect" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required>
                <button type="submit">Detect Objects</button>
            </form>
            <div id="result"></div>
        </body>
    </html>
    """


@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    """
    Handle image upload and forward to AI backend
    
    Returns:
        Detection results from AI service
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Forward to AI backend
        contents = await file.read()
        files = {"file": (file.filename, contents, file.content_type)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{AI_BACKEND_URL}/predict",
                files=files
            )
            response.raise_for_status()
            
        return response.json()
        
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"AI service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """Service health check"""
    return {"status": "healthy"}
