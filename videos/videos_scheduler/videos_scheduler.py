from apscheduler.schedulers.background import BackgroundScheduler
from videos.views import fetch_videos_function

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(fetch_videos_function, "interval", seconds=10, id="videos_001",replace_existing=True)
	scheduler.start()
