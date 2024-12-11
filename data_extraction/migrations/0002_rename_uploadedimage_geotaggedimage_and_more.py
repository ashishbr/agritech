# Generated by Django 5.1.4 on 2024-12-10 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_extraction', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UploadedImage',
            new_name='GeotaggedImage',
        ),
        migrations.RenameField(
            model_name='geotaggedimage',
            old_name='extracted_data',
            new_name='extracted_text',
        ),
        migrations.RenameField(
            model_name='geotaggedimage',
            old_name='timestamp',
            new_name='uploaded_at',
        ),
    ]