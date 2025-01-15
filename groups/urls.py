from django.urls import path
from groups import views

urlpatterns = [
    path('groups/', views.LikeList.as_view()),
    #path('likes/<int:pk>/', views.LikeDetail.as_view()),
]