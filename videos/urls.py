from django.urls import path, re_path
from videos import views

app_name = "videos"
urlpatterns = [
    path('get_videos', views.get_videos.as_view(), name="get_videos")
]