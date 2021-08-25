from django.apps import AppConfig

class VideosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videos'

    def ready(self):
        print("Starting Videos Scheduler ...")
        from videos.videos_scheduler import videos_scheduler
        videos_scheduler.start()