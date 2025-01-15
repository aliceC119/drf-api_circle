from django.db import models
from django.contrib.auth.models import User
from groups.models import Group
from cloudinary_storage.storage import MediaCloudinaryStorage
from .validators import validate_youtube_url


class Post(models.Model):
    
    """
    Post model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """
    image_filter_choices = [
    ('_1977', '1977'), ('brannan', 'Brannan'),
    ('earlybird', 'Earlybird'), ('hudson', 'Hudson'),
    ('inkwell', 'Inkwell'), ('lofi', 'Lo-Fi'),
    ('kelvin', 'Kelvin'), ('normal', 'Normal'),
    ('nashville', 'Nashville'), ('rise', 'Rise'),
    ('toaster', 'Toaster'), ('valencia', 'Valencia'),
    ('walden', 'Walden'), ('xpro2', 'X-pro II')
]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_mgvuq6', blank=True
    )
    image_filter = models.CharField(
        max_length=32, choices=image_filter_choices, default='normal'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'

class VideoPost(models.Model):

    video_filter_choices = [ 
    ('normal', 'Normal'), ('sepia', 'Sepia'), ('grayscale', 'Grayscale')
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video = models.FileField( 
        upload_to='video/', blank=True, storage=MediaCloudinaryStorage())
    video_filter = models.CharField( 
        max_length=32, choices=video_filter_choices, default='normal' )
    youtube_url = models.URLField( 
        validators=[validate_youtube_url], blank=True, null=True )
    #likes = models.PositiveIntegerField(default=0)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'


class SharedPost(models.Model):
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shared_posts')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.shared_by.username} shared: {self.original_post.content[:50]}"