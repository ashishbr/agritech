from django.db import models

class GeotaggedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
