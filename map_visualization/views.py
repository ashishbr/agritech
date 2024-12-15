from django.shortcuts import render
from django.http import JsonResponse
from data_extraction.models import GeotaggedImage
import re  # To use regex for extraction

def get_geotagged_data(request):
    """
    Extract latitude, longitude, farmer name, and notes from extracted_text field
    and return as JSON.
    """
    # Regular expressions for extracting relevant data
    lat_pattern = r"Latitude:\s*([+-]?\d*\.\d+)"          # Match latitude
    lng_pattern = r"Longitude:\s*([+-]?\d*\.\d+)"        # Match longitude
    farmer_name_pattern = r"Farmer Name:\s*([\w\s]+)"    # Match farmer name
    note_pattern = r"Note:\s*(.*)"                       # Match note after 'Note:'

    parsed_data = []

    # Fetch all records with extracted_text
    geotagged_images = GeotaggedImage.objects.exclude(extracted_text__isnull=True)

    for image in geotagged_images:
        text = image.extracted_text
        if text:
            # Extract latitude and longitude
            lat_match = re.search(lat_pattern, text)
            lng_match = re.search(lng_pattern, text)

            if lat_match and lng_match:
                latitude = float(lat_match.group(1))
                longitude = float(lng_match.group(1))

                # Extract farmer name and note
                farmer_name_match = re.search(farmer_name_pattern, text)
                note_match = re.search(note_pattern, text)

                farmer_name = farmer_name_match.group(1).strip() if farmer_name_match else "Unknown"
                note = note_match.group(1).strip() if note_match else "No note available"

                # Append extracted data to the response list
                parsed_data.append({
                    "latitude": latitude,
                    "longitude": longitude,
                    "farmer_name": farmer_name,
                    "note": note,
                })

    return JsonResponse(parsed_data, safe=False)