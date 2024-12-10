from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    extracted_data = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.timestamp}"
