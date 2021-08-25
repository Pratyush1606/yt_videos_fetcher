from django.db import models

# Create your models here.
class Video(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    thumbnails_url = models.URLField()
    publishing_datetime = models.DateTimeField()

    class Meta:
        ordering = ('-publishing_datetime',)

    def __str__(self):
        return "{}, {}".format(self.id, self.title)