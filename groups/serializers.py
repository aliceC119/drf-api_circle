from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Group
from posts.models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    media_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'group', 'owner', 'content', 'media_url', 'created_at']

    def get_media_url(self, obj):
        return obj.media_file.url if obj.media_file else None

class GroupSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField( 
        many=True, 
        queryset=User.objects.all(), 
        slug_field='username' )
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'members', 'posts']
