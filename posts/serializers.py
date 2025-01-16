from rest_framework import serializers
from posts.models import Post, VideoPost, SharedPost
from likes.models import Like
from .validators import validate_youtube_url
import cloudinary 
import cloudinary.uploader



def upload(video):
    try:
        result = cloudinary.uploader.upload(video, resource_type="video")
        print(f"Upload result: {result}")
        return result['secure_url']
    except cloudinary.exceptions.Error as e:
        print(f"Cloudinary upload error: {e}")
        raise serializers.ValidationError("Failed to upload video to Cloudinary.")

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'image_filter',
            'like_id', 'likes_count', 'comments_count',
        ]

class VideoPostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    video = serializers.FileField(required=False)
    youtube_url = serializers.URLField(required=False, validators=[validate_youtube_url])

    MAX_VIDEO_SIZE = 10 * 1024 * 1024 * 1024 # 10 GB in bytes 
    MAX_RESOLUTION_WIDTH = 1280 
    MAX_RESOLUTION_HEIGHT = 720
    ALLOWED_FILE_TYPES = ['video/mp4', 'video/quicktime'] # mp4 and mov


    
    def validate_video(self, value): 
        if value.size > self.MAX_VIDEO_SIZE: 
            raise serializers.ValidationError("Video size should not exceed 10GB.") 

        if value.content_type not in self.ALLOWED_FILE_TYPES: 
            raise serializers.ValidationError("Unsupported file type. Only MP4 and MOV are allowed.") 
        
        return value
    
    
    
    def validate(self, data): 
        video = data.get('video', None) 
        youtube_url = data.get('youtube_url', None) 
        
        if not video and not youtube_url: 
            raise serializers.ValidationError("Either video or youtube_url must be provided.") 
        
        # Explicitly call the field-specific validation method 
        if video: 
            self.validate_video(video) 
        return data
 
    def create(self, validated_data): 
        video = validated_data.get('video') 
        if video: 
            validated_data['video_url'] = upload(video) 
        return super().create(validated_data)
      

    def validate_media_file(self, value):
        """
        Check that the media file is either an image or a video.
        """
        if value.content_type.startswith('image'):
            return value
        elif value.content_type.startswith('video'):
            return value
        else:
            raise serializers.ValidationError("Unsupported file type. Only images and videos are allowed.")

    def get_is_owner(self, obj): 
        request = self.context.get('request') 
        if request and request.user: 
            return obj.owner == request.user 
        return False
    
    def get_like_id(self, obj): 
        user = self.context['request'].user 
        if user.is_authenticated: 
            like = Like.objects.filter(owner=user, video_post=obj).first() 
            return like.id if like else None 
        return None

    class Meta:
        model = VideoPost
        fields = [
            'id','owner', 'created_at', 'updated_at', 'title',
            'description', 'video', 'video_filter', 'profile_image',
            'is_owner', 'like_id', 'likes_count', 'comments_count',
            'profile_id','youtube_url',
        ]
    
class SharedPostSerializer(serializers.ModelSerializer): 
    class Meta:
         model = SharedPost 
         fields = [
            'original_post', 'shared_by', 'created_at'
        ]