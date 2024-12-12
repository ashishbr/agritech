from django.shortcuts import render
from data_extraction.models import GeotaggedImage
from django.http import JsonResponse
import re

# Function to extract latitude and longitude from extracted_text
def parse_coordinates(text):
    # Regex pattern to extract latitude and longitude
    pattern = r"([-+]?\d{1,2}\.\d+),\s*([-+]?\d{1,3}\.\d+)"
    match = re.search(pattern, text)
    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return latitude, longitude
    return None, None

# View to get geotagged data dynamically
def get_geotagged_data(request):
    data = []
    for record in GeotaggedImage.objects.all():
        latitude, longitude = parse_coordinates(record.extracted_text or "")
        if latitude is not None and longitude is not None:
            data.append({
                'latitude': latitude,
                'longitude': longitude,
                'farmer_name': record.farmer_name,  # Ensure this field exists or adapt as needed
                'note': record.note,               # Ensure this field exists or adapt as needed
            })
    return JsonResponse(data, safe=False)