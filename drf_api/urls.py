"""drf_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from groups.views import GroupViewSet
from posts.views import PostList, PostDetail, VideoPost, VideoPostDetail

router = DefaultRouter() 
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/posts/', PostList.as_view(), name='post-list'), 
    path('api/posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('api/videoposts/', PostList.as_view(), name='videopost-list'), 
    path('api/videoposts/<int:pk>/', VideoPostDetail.as_view(), name='videopost-detail'),
    path('', include('profiles.urls')),
    path('', include('posts.urls')),
    path('', include('likes.urls')),
    path('', include('comments.urls')),
    path('', include('followers.urls')),
]