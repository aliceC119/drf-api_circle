# Generated by Django 4.2 on 2025-01-14 23:16

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_remove_videopost_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videopost',
            name='video',
            field=models.FileField(blank=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='video/'),
        ),
    ]
