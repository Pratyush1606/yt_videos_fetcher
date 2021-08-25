# YOUTUBE VIDEOS FETCHER

**yt_videos_fetcher** is a Django application which continuously fetches latest videos sorted in reverse chronological order of their publishing date-time from *YouTube* for a given tag/search query in a paginated response.

---

## **Technologies**

* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Rest APIs with [Django](https://www.djangoproject.com/)
* Database used: [SQLite](https://www.sqlite.org/index.html) (for development)

---

## **API Reference**

### **GET** /videos/get_videos

This API returns the stored video data in a paginated response sorted in descending order of published datetime.

**Example Request**

```js
GET {site}/videos/get_videos
```

**Example Successful Response**

***Status Code***

`200`

Response will be in paginated form.

```json
{
    "count": 26,
    "next": "http://127.0.0.1:8000/videos/get_videos?p=2",
    "previous": null,
    "results": [
        {
            "id": "K9SjH8Agi9s",
            "title": "SkRossi VLOGS - How Not to play Cricket VLOG #2",
            "description": "Global Esports Valorant Athlete: SKRossi (Ganesh) On this channel, I play Valorant live and sometimes other games as well. I am a part of the Indian Esports ...",
            "thumbnails_url": "https://i.ytimg.com/vi/K9SjH8Agi9s/mqdefault.jpg",
            "publishing_datetime": "2021-08-25T12:30:11Z"
        },
        {
            "id": "k4YSs78_bFs",
            "title": "India vs England Cricket Test Highlights | 3rd Test, Day 1 | Cricket Highlights 08/25/2021 P2",
            "description": "India #England #Cricket #3rdTest #Test India vs England Cricket Test Full-Match Highlights | 3rd Test, Day 1 | Cricket Highlights 08/25/2021 England vs India ...",
            "thumbnails_url": "https://i.ytimg.com/vi/k4YSs78_bFs/mqdefault.jpg",
            "publishing_datetime": "2021-08-25T11:22:22Z"
        },
        {
            "id": "pXwsuHmZvL0",
            "title": "India vs England 3rd Test Highlights | Day 1 | Cricket Highlights | IND vs ENG 08/25/2021 P2",
            "description": "Cricket #India #England India vs England 3rd Test Highlights | Day 1 | Cricket Highlights | IND vs ENG 08/25/2021 England vs India 3rd Test Highlights | Day 1 ...",
            "thumbnails_url": "https://i.ytimg.com/vi/pXwsuHmZvL0/mqdefault.jpg",
            "publishing_datetime": "2021-08-25T11:14:14Z"
        }
    ]
}
```

### **GET** /videos/search_videos

This API returns the stored video data in a paginated response sorted in descending order of published datetime.

**Example Request**

```js
GET {site}/videos/search_videos?query={string_to_be_searched}
```

***parameters***

```json
"query": "string to be searched"
```

**Example Successful Response**

***Status Code***

`200`

***Body***

```json
[
    {
        "id": "K9SjH8Agi9s",
        "title": "SkRossi VLOGS - How Not to play Cricket VLOG #2",
        "description": "Global Esports Valorant Athlete: SKRossi (Ganesh) On this channel, I play Valorant live and sometimes other games as well. I am a part of the Indian Esports ...",
        "thumbnails_url": "https://i.ytimg.com/vi/K9SjH8Agi9s/mqdefault.jpg",
        "publishing_datetime": "2021-08-25T12:30:11Z"
    },
    {
        "id": "k4YSs78_bFs",
        "title": "India vs England Cricket Test Highlights | 3rd Test, Day 1 | Cricket Highlights 08/25/2021 P2",
        "description": "India #England #Cricket #3rdTest #Test India vs England Cricket Test Full-Match Highlights | 3rd Test, Day 1 | Cricket Highlights 08/25/2021 England vs India ...",
        "thumbnails_url": "https://i.ytimg.com/vi/k4YSs78_bFs/mqdefault.jpg",
        "publishing_datetime": "2021-08-25T11:22:22Z"
    },
    {
        "id": "pXwsuHmZvL0",
        "title": "India vs England 3rd Test Highlights | Day 1 | Cricket Highlights | IND vs ENG 08/25/2021 P2",
        "description": "Cricket #India #England India vs England 3rd Test Highlights | Day 1 | Cricket Highlights | IND vs ENG 08/25/2021 England vs India 3rd Test Highlights | Day 1 ...",
        "thumbnails_url": "https://i.ytimg.com/vi/pXwsuHmZvL0/mqdefault.jpg",
        "publishing_datetime": "2021-08-25T11:14:14Z"
    },
    {
        "id": "7rnnocl8gNU",
        "title": "India vs England Cricket Test Highlights | 3rd Test, Day 1 | Cricket Highlights 08/25/2021",
        "description": "India #England #Cricket #3rdTest #Test India vs England Cricket Test Full-Match Highlights | 3rd Test, Day 1 | Cricket Highlights 08/25/2021 England vs India ...",
        "thumbnails_url": "https://i.ytimg.com/vi/7rnnocl8gNU/mqdefault.jpg",
        "publishing_datetime": "2021-08-25T10:39:09Z"
    }
]
```

---

## **Local Setup**

* If you wish to run your own build, first ensure you have python3 globally installed in your computer. If not, you can get python [here](https://www.python.org/downloads/).

* Clone the repository

  * Using HTTPS

    ```sh
    git clone https://github.com/Pratyush1606/yt_videos_fetcher.git
    ```
  
  * Using SSH

    ```sh
    git clone git@github.com:Pratyush1606/yt_videos_fetcher.git
    ```

* Download [pip](https://pip.pypa.io/en/stable/installing/) and add it to the path

* Change your working directory to the the cloned folder

    ```bash
    cd path/to/yt_videos_fetcher
    ```

* Download all the dependencies

    ```bash
    pip install -r requirements.txt
    ```

    Use `pip3` if `pip` not working

* Download all the dependencies

    ```bash
    pip install -r requirements.txt
    ```

* Make a ``base_settings.py`` file in the project folder directory (at the project settings.py level) and put all the ***API KEYS*** in a list `API_KEY_LIST` obtained from the Google API Console, Django ***SECRET_KEY*** and ***DEBUG*** mode as below

    ```python
    DEBUG = True
    API_KEY_LIST = ["xxxxxxxxxxxx91", "yyyyyyyyyyyyy"]
    SECRET_KEY = 'django-insecure-sifi0)i0$al(xa&p1uulpq)2-qxy!xcqw%a=-x$+*h**#6rrq'
    ```

  * While putting `DEBUG = False`, remember to modify `ALLOWED_HOSTS` (for just quick reference, modify as `ALLOWED_HOSTS = ['*']`)

  * Put at least one ***API KEY*** in `API_KEY_LIST` otherwise there won't be any entry in database

  * For generating a Django SECRET_KEY, many different sites are there. This [site](https://miniwebtool.com/django-secret-key-generator/) can be used for quick reference.

### Before proceeding further, make sure ```Directory``` looks like

```
yt_videos_fetcher
├── videos
|    ├── migrations
|    ├── videos_scheduler
|    |    ├── __init__.py
|    |    └── videos_scheduler.py
|    ├── __init__.py
|    ├── admin.py
|    ├── apps.py
|    ├── models.py
|    ├── pagination.py
|    ├── serializers.py
|    ├── tests.py
|    ├── urls.py
|    └── views.py
├── yt_videos_fetcher
|   ├── __init__.py
|   ├── settings.py
|   ├── asgi.py
|   ├── base_settings.py
|   ├── wsgi.py
|   └── urls.py
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

* Migrate to the database

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

    Use `python3` if `python` not working

    After this, you would see a new file named `db.sqlite3` in your parent folder

* Run server

    ```sh
    python manage.py runserver
    ```
