# Generated by Django 5.1.4 on 2024-12-11 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_extraction', '0002_rename_uploadedimage_geotaggedimage_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geotaggedimage',
            old_name='uploaded_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='geotaggedimage',
            name='extracted_text',
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='accuracy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='crop_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='elevation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='farmer_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='farmer_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='saplings',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='tahsil',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='geotaggedimage',
            name='village',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]