from django.shortcuts import render, redirect
from .models import GeotaggedImage
from .forms import ImageUploadForm
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image


def index(request):
    return render(request, 'data_extraction/index.html', {})

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()  # Save the image to the database
            
            # Perform OCR using Google Cloud Vision
            client = vision.ImageAnnotatorClient()
            
            # Read the uploaded image file
            with open(image_instance.image.path, 'rb') as image_file:
                content = image_file.read()
            
            # Create an Image object for Vision API
            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            annotations = response.text_annotations
            
            # Extract the detected text
            if annotations:
                extracted_text = annotations[0].description
            else:
                extracted_text = "No text detected"

            # Save the extracted text to the database
            image_instance.extracted_text = extracted_text
            image_instance.save()

            return redirect('image_list')
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})


def image_list(request):
    images = GeotaggedImage.objects.all()
    return render(request, 'image_list.html', {'images': images})