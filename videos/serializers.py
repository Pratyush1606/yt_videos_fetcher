from rest_framework import serializers
from videos.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'thumbnails_url', 'publishing_datetime']
