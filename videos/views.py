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

def fetch_videos_function():
    url = "https://youtube.googleapis.com/youtube/v3/search"
    publishedAfter = (timezone.now() - timedelta(weeks=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    params = {
        "part": "snippet",
        "order": "date",
        "q": "cricket",
        "type": "video",
        "maxResults": 50,   # Taking maximum of 50 results in one page (max allowed=50)
        "publishedAfter": publishedAfter,
        "key": API_KEY_LIST[0]
    }
    no_of_pages = 2     # Taking only 2 pages (means total of 100 results)
    for API_KEY in API_KEY_LIST:
        params["key"] = API_KEY
        resp = requests.get(url, params=params)
        if(resp.status_code==200):
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

class search_videos(APIView):

    def search_algorithm(self, query):
        videos = Video.objects.all()
        corpus = VideoSerializer(videos, many=True).data
        import nltk
        # remove stop words and tokenize them (we probably want to do some more
        # preprocessing with our text in a real world setting, but we'll keep
        # it simple here)
        stopwords = ["you've", 'was', 'to', 'until', 'will', 'while', 'more', "don't", "hasn't", 'being', 'they', 'if', 'same', 'whom', 'can', 'each', 'we', 'haven', 'then', 'his', 'don', 'ourselves', "won't", 'both', 'off', 'y', "it's", 'up', 'didn', 'herself', 's', "needn't", 'too', 'when', 'between', 'do', 'not', 'ain', "shouldn't", 'having', 'does', 'some', 'ma', 'shouldn', 'out', 'all', 'am', 'which', 'these', 'theirs', 'mustn', 'nor', 'own', 'any', 'further', 'needn', 'under', 'as', 'above', 'himself', 'below', 'o', 'because', 'is', 'on', 'did', 'd', 'so', 'won', 'how', 'itself', "that'll", 'before', 'of', 'what', 'such', 'myself', 'your', 'doing', 'no', "you're", "you'd", 'our', 'here', 'only', 'its', 'down', 'weren', 'been', 'that', 'her', 'you', "she's", "isn't", "shan't", "doesn't", 'this', 'hadn', 'him', 'has', 'those', 'had', 'other', 'ours', 'against', "haven't", 't', "wouldn't", 'than', 'aren', "mightn't", 'it', "wasn't", 'or', 'the', 'wasn', 'have', "you'll", 'are', 'hers', 'she', 'my', 'in', 'an', 'few', 'for', 'over', 'couldn', 'doesn', 'shan', 'who', 'wouldn', 'now', "aren't", 'about', "mustn't", 'from', 've', 'very', "couldn't", 'mightn', 'again', 'but', 'into', 'just', 'with', 'a', 'by', "didn't", "should've", 'be', 'themselves', 'he', 'yours', 'i', 'them', 'their', 'yourself', 'where', 'after', 'isn', "weren't", 'me', 'through', 'hasn', 'yourselves', 'during', 'at', 'why', 'should', 'most', 'm', 'once', 'were', 're', 'and', "hadn't", 'there', 'll']
        words = set(nltk.corpus.words.words())
        trim_non_english_chars = (lambda sent: " ".join(w for w in nltk.wordpunct_tokenize(sent) if w.lower() in words or not w.isalpha()))
        
        # Combining title and description altogether after trimming non english chars 
        # and then removing stopwords
        texts = [[word for word in trim_non_english_chars(video["title"]+" "+video["description"]).lower().split() if word not in stopwords] for video in corpus]

        # # building a word count dictionary so we can remove words that appear only once
        # word_count_dict = {}
        # for text in texts:
        #     for token in text:
        #         word_count = word_count_dict.get(token, 0) + 1
        #         word_count_dict[token] = word_count

        # texts = [[token for token in text if word_count_dict[token] > 1] for text in texts]

        video_id_score = []
        query = [word for word in trim_non_english_chars(query).lower().split() if word not in stopwords]
        from rank_bm25 import BM25Okapi
        try:
            bm25 = BM25Okapi(texts)
            scores = list(bm25.get_scores(query))

            # Storing query search score for all videos
            for score, doc in zip(scores, corpus):
                score = round(score, 3)
                video_id_score.append([doc["id"], score])
        except Exception as e:
            return []

        # Sorting videos based on the search score
        video_id_score.sort(key=lambda x: x[1], reverse=True)
        # Taking 20 most relevant searches
        most_relevant_videos_id_list = [id for id, score in video_id_score[:20]]
        return most_relevant_videos_id_list
    
    def get(self, request):
        query = request.GET.get("query", None)
        if(not query):
            return Response(data=[], status=status.HTTP_200_OK)
        most_relevant_videos_id_list = self.search_algorithm(query)
        videos = Video.objects.filter(id__in=most_relevant_videos_id_list)
        data = VideoSerializer(videos, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)