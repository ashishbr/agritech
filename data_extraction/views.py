import cv2
import numpy as np
from django.shortcuts import render, redirect
from .models import GeotaggedImage
from .forms import ImageUploadForm
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image
from .utils import perform_ocr, detect_multiple_images

def index(request):
    return render(request, 'data_extraction/index.html', {})

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()  # Save the image to the database
            
            # Initialize Vision API client
            client = vision.ImageAnnotatorClient()
            
            image_path = image_instance.image.path
            bounding_boxes = detect_multiple_images(image_path)
            
            ocr_results = []
            
            if bounding_boxes:
                # Multiple images detected; process each region separately
                image = cv2.imread(image_path)
                for idx, (x, y, w, h) in enumerate(bounding_boxes):
                    cropped = image[y:y+h, x:x+w]
                    
                    # Save cropped region to temporary file
                    temp_path = f"{image_path}_part_{idx}.jpg"
                    cv2.imwrite(temp_path, cropped)
                    
                    with open(temp_path, 'rb') as image_file:
                        content = image_file.read()
                    extracted_text = perform_ocr(client, content)
                    
                    # Only append to results if the extracted text is not None or empty
                    if extracted_text:
                        ocr_results.append(f"Image {idx+1}:\n{extracted_text}")
            else:
                # Single image; process the whole image
                with open(image_path, 'rb') as image_file:
                    content = image_file.read()
                extracted_text = perform_ocr(client, content)
                
                # Only append to results if the extracted text is not None or empty
                if extracted_text:
                    ocr_results.append(f"{extracted_text}")
            
            # Combine results and save to database
            if ocr_results:  # Only save if there are valid OCR results
                combined_text = "\n\n".join(ocr_results)
                image_instance.extracted_text = combined_text
                image_instance.save()

            return redirect('image_list')
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})


def image_list(request):
    images = GeotaggedImage.objects.all()
    return render(request, 'image_list.html', {'images': images})