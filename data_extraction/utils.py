import os
import cv2
import numpy as np
from django.shortcuts import render, redirect
from .models import GeotaggedImage
from .forms import ImageUploadForm
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image
from google.cloud import secretmanager, vision

def get_google_credentials_from_secret(secret_id, project_id):
    """
    Fetch the Google Application Credentials JSON from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=secret_name)

    # The payload contains the secret in bytes
    secret_payload = response.payload.data.decode("UTF-8")

    # Write the secret to a temporary file
    temp_cred_path = "/tmp/google_credentials.json"
    with open(temp_cred_path, "w") as cred_file:
        cred_file.write(secret_payload)

    return temp_cred_path

def detect_multiple_images(image_path):
    """
    Check if an image contains multiple regions (sub-images).
    """
    # Load image and preprocess
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)  # Edge detection

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter out small noise
    valid_contours = [c for c in contours if cv2.contourArea(c) > 1000]
    
    # Return bounding boxes if multiple valid contours exist
    if len(valid_contours) > 1:
        return [cv2.boundingRect(c) for c in valid_contours]
    return None

def perform_ocr(client, image_content):
    """
    Performs OCR using Google Vision API.
    """
    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)
    annotations = response.text_annotations
    if annotations:
        return annotations[0].description
    return None
