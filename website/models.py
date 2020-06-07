from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    close_date = models.DateField()  # the close_date will be the last day on which the post is visible on the website

    def __str__(self):
        return self.title

    @property
    def is_closed(self):
        return timezone.now().date() > self.close_date

    @property
    def is_open(self):
        return not self.is_closed()


class YouTubeVideo(models.Model):
    title = models.CharField(max_length=64)
    video_id = models.CharField(max_length=64)
    upload_datetime = models.DateTimeField()
    show_on_website = models.BooleanField()

    class Meta:
        verbose_name = 'YouTube video'
        verbose_name_plural = 'YouTube videos'

    def __str__(self):
        return self.title

    def get_embed_link(self):
        return 'https://www.youtube.com/embed/' + self.video_id

    def get_video_link(self):
        return 'https://www.youtube.com/watch?v=' + self.video_id
