from django.db.models import Count
from rest_framework import generics, permissions, filters, status
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post, VideoPost, SharedPost
from .serializers import PostSerializer,VideoPostSerializer, SharedPostSerializer
import cloudinary 
import cloudinary.uploader




    
class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        user = self.request.user
        media_file = self.request.FILES.get('media_file') 
        if media_file: 
            # Determine the media type 
            if media_file.content_type.startswith('image'): 
                media_type = 'image' 
            elif media_file.content_type.startswith('video'): 
                media_type = 'video' 
            else: 
                raise serializers.ValidationError("Unsupported file type.") 
            
            serializer.save(owner=self.request.user, media_type=media_type, media_file=media_file) 
        else: 
            serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')


class VideoPostList(generics.ListCreateAPIView):
    """
    List videoposts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = VideoPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = VideoPost.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]
    def post(self, request, *args, **kwargs): 
        serializer = VideoPostSerializer(data=request.data, context={'request': request}) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer): 
        user = self.request.user 
        media_file = self.request.FILES.get('media_file')
        if media_file: 
            if media_file.content_type.startswith('image'): 
                media_type = 'image' 
            elif media_file.content_type.startswith('video'): 
                media_type = 'video' 
            else: 
                    raise serializers.ValidationError("Unsupported file type.") 
            serializer.save(owner=user, media_type=media_type, media_file=media_file) 
        else: 
            serializer.save(owner=user)
    

    def post(self, request, *args, **kwargs):
        serializer = VideoPostSerializer(data=request.data, context={'request': request}) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoPostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a video post and edit or delete it if you own it.
    """
    serializer_class = VideoPostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = VideoPost.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-created_at')

class SharedPostList(generics.ListCreateAPIView): 
    
    serializer_class = SharedPostSerializer
    queryset = SharedPost.objects.all()

class SharedPostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a shared post and edit or delete it if you own it.
    """
    serializer_class = SharedPostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = SharedPost.objects.all()