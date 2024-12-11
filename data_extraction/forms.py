from django import forms
from .models import GeotaggedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = GeotaggedImage
        fields = ('image', )
