from django.db import models
from django.contrib.auth.models import User
from posts.models import Post, VideoPost, SharedPost, SharedVideoPost


class Like(models.Model):
    """
    Like model, related to 'owner' and 'post'.
    'owner' is a User instance and 'post' is a Post instance.
    'unique_together' makes sure a user can't like the same post twice.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='likes', on_delete=models.CASCADE, null=True, blank=True
    )
    video_post = models.ForeignKey(
        VideoPost, related_name='likes', on_delete=models.CASCADE, null=True, blank=True
    )
    shared_post = models.ForeignKey( 
        SharedPost, related_name='likes', on_delete=models.CASCADE, null=True, blank=True 
    ) 
    shared_video_post = models.ForeignKey( 
        SharedVideoPost, related_name='likes', on_delete=models.CASCADE, null=True, blank=True 
    )
   
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'post', 'video_post', 'shared_post', 'shared_video_post']

    def __str__(self):
        return f'{self.owner} {self.post} {self.video_post} {self.shared_post} {self.shared_video_post}'