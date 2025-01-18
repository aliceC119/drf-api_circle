from django.urls import path
from posts import views


urlpatterns = [
    
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('video-posts/', views.VideoPostList.as_view()),
    path('video-posts/<int:pk>/', views.VideoPostDetail.as_view()),
    path('shared-posts/', views.SharedPostList.as_view()),
    path('shared-posts/<int:pk>/', views.SharedPostDetail.as_view()),
    path('shared-video-posts/', views.SharedVideoPostList.as_view()), 
    path('shared-video-posts/<int:pk>/', views.SharedVideoPostDetail.as_view()),

]