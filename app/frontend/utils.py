import os
import requests
import streamlit as st
from PIL import Image
import io

API_URL = "http://127.0.0.1:8000/predict"

def call_prediction_api(image_file):
    """
    Calls the FastAPI backend for prediction.
    """
    try:
        # Reset file pointer
        image_file.seek(0)
        files = {"file": (image_file.name, image_file, "image/jpeg")}
        
        response = requests.post(API_URL, files=files, timeout=120)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error from server: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        st.error("API Error: Request timed out. Is the backend running?")
        return None
    except requests.exceptions.ConnectionError:
        st.error("API Error: Could not connect to the backend. Please ensure the FastAPI server is running at http://127.0.0.1:8000")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None

def format_confidence(confidence):
    """Formats confidence score as a percentage string"""
    return f"{confidence:.2f}%"

def get_image_info(image_file):
    """Extracts image metadata"""
    img = Image.open(image_file)
    width, height = img.size
    
    # Get file size in MB
    image_file.seek(0, 2)
    file_size_bytes = image_file.tell()
    file_size_mb = file_size_bytes / (1024 * 1024)
    image_file.seek(0)
    
    return {
        "filename": image_file.name,
        "resolution": f"{width}x{height}",
        "size": f"{file_size_mb:.2f} MB"
    }

def process_image_for_display(image_file):
    """Returns a PIL Image object from uploaded file"""
    image_file.seek(0)
    return Image.open(image_file)
