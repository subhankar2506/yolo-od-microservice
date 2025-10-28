#!/usr/bin/env python3
"""
Simple test script for object detection service
Usage: python test_detection.py <image_path>
"""

import sys
import requests
from pathlib import Path


def test_detection(image_path):
    """Test object detection with a local image"""
    if not Path(image_path).exists():
        print(f"Error: Image not found at {image_path}")
        return
    
    url = "http://localhost:8000/detect"
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nDetection successful!")
        print(f"Objects found: {result['count']}\n")
        
        for i, det in enumerate(result['detections'], 1):
            print(f"{i}. {det['class']}")
            print(f"   Confidence: {det['confidence']:.2f}")
            print(f"   BBox: {det['bbox']}\n")
        
        # Display output file locations
        if 'annotated_image' in result:
            print("Output Files:")
            print(f"  Annotated Image: http://localhost:8001{result['annotated_image']}")
            print(f"  JSON File: http://localhost:8001{result['json_file']}")
            print(f"\n  Local files saved in: ./outputs/")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_detection.py <image_path>")
        sys.exit(1)
    
    test_detection(sys.argv[1])
