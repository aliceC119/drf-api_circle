# Generated by Django 4.2 on 2025-01-14 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_videopost_comments_videopost_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videopost',
            name='likes',
        ),
    ]
