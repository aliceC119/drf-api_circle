# Generated by Django 4.2 on 2025-01-14 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_videopost_youtube_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='videopost',
            name='comments',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='videopost',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
