from rest_framework import serializers
from posts.models import Post, VideoPost, SharedPost
from likes.models import Like


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

    def validate_video(file): 
        valid_mime_types = ['video/mp4', 'video/avi', 'video/mov'] 
        max_file_size = 1920 * 1080 * 5120 #1920 x 1080 px 5GB

        if file.content_type not in valid_mime_types: 
            raise ValidationError('Unsupported file type.') 

        if file.size > max_file_size: 
            raise ValidationError('File too large. Size should not exceed 5 GB.') 
            
            return file


    class Meta:
        model = VideoPost
        fields = [
            'owner', 'created_at', 'updated_at', 'title',
            'description', 'video', 'video_filter', 'profile_image',
            'is_owner', 'like_id', 'likes_count', 'comments_count',
            'profile_id'
        ]

class SharedPostSerializer(serializers.ModelSerializer): 
    class Meta:
         model = SharedPost 
         fields = [
            'original_post', 'shared_by', 'created_at'
        ]