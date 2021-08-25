from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.conf import settings
import requests
from datetime import timedelta

from videos.models import Video
from videos.serializers import VideoSerializer
from videos.pagination import CustomPagination, MyPaginationMixin

API_KEY_LIST = settings.API_KEY_LIST

def save_videos(videos):
    for video in videos:
        id = video["id"]["videoId"]
        video_already_exists = Video.objects.filter(id=id).exists()
        if(video_already_exists):
            # Video already exists in database
            continue

        # New video which doesn't exist in database
        snippet = video["snippet"]
        title = snippet["title"]
        description = snippet["description"]
        thumbnails_url = snippet["thumbnails"]["medium"]["url"]
        publishing_datetime = snippet["publishedAt"]
        data = {
            "id": id,
            "title": title,
            "description": description,
            "thumbnails_url": thumbnails_url,
            "publishing_datetime": publishing_datetime
        }
        serializer = VideoSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
    print(len(Video.objects.all()))

def fetch_videos_function():
    url = "https://youtube.googleapis.com/youtube/v3/search"
    publishedAfter = (timezone.now() - timedelta(weeks=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    params = {
        "part": "snippet",
        "order": "date",
        "q": "cricket",
        "type": "video",
        "maxResults": 2,   # Taking maximum of 50 results in one page (max allowed=50)
        "publishedAfter": publishedAfter,
        "key": API_KEY_LIST[0]
    }
    no_of_pages = 10     # Taking only 2 pages (means total of 100 results)
    for API_KEY in API_KEY_LIST:
        params["key"] = API_KEY
        resp = requests.get(url, params=params)
        if(resp.status_code==200):
            print(API_KEY)
            # It means that this API has not reached its daily quota 
            # and it can be used to make further requests
            # And once the required requests have been made, this outer loop execution will stop
            curr_no_of_pages = 1
            resp_body = resp.json()
            next_page_token = resp_body["nextPageToken"]
            videos = resp_body["items"]
            save_videos(videos)

            while(curr_no_of_pages<no_of_pages and (next_page_token)):
                curr_no_of_pages += 1
                params["pageToken"] = next_page_token
                resp = requests.get(url, params=params)
                if(resp.status_code==200):
                    resp_body = resp.json()
                    next_page_token = resp_body["nextPageToken"]
                    videos = resp_body["items"]
                    save_videos(videos)
                else:
                    break
            # All the required requests have been made and videos have been saved
            # So, this outer loop execution has to stop
            break

class get_videos(APIView, MyPaginationMixin):
    pagination_class = CustomPagination

    def get(self, request):
        videos = Video.objects.all()
        page = self.paginate_queryset(videos)

        if page is not None:
            serializers = VideoSerializer(page, many=True)
            return self.get_paginated_response(serializers.data)

        serializers = VideoSerializer(videos, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)