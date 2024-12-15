from django.shortcuts import render, redirect
from .models import GeotaggedImage
from .forms import ImageUploadForm
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image
from .utils import get_google_credentials_from_secret


def index(request):
    return render(request, 'data_extraction/index.html', {})

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()  # Save the image to the database
            
            # Set GOOGLE_APPLICATION_CREDENTIALS 
            secret_id = "newgooglevisionsecretkey"  # secret name
            project_id = "595045753872"  # project ID
            credentials_path = get_google_credentials_from_secret(secret_id, project_id)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            
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