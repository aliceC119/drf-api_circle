import re
from django.core.exceptions import ValidationError

YOUTUBE_REGEX = re.compile(
    r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
)

def validate_youtube_url(value):
    if not YOUTUBE_REGEX.match(value):
        raise ValidationError("This is not a valid YouTube URL.")
