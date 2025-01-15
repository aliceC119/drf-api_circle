from django.urls import path
from posts import views


urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('video-posts/', views.VideoPostList.as_view()),
    path('videoposts/<int:pk>/', views.VideoPostDetail.as_view()),
    path('shared-posts/', views.SharedPostList.as_view())
]