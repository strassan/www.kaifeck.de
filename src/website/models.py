from django.db import models
from django.utils import timezone
from datetime import datetime

from googleapiclient.discovery import build


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    close_date = models.DateField()  # the close_date will be the last day on which the post is visible on the website

    def __str__(self):
        return self.title

    def is_closed(self):
        return timezone.now().date() > self.close_date

    def is_open(self):
        return not self.is_closed()


class YouTubeVideo(models.Model):
    title = models.CharField(max_length=64)
    video_id = models.CharField(max_length=64)
    upload_datetime = models.DateTimeField()
    show_on_website = models.BooleanField()

    def __str__(self):
        return self.title

    def get_embed_link(self):
        return 'https://www.youtube.com/embed/' + self.video_id

    def get_video_link(self):
        return 'https://www.youtube.com/watch?v=' + self.video_id

    @staticmethod
    def get_youtube_uploads(channel_id='UCU5yJUgbF9E2LxDLS-voY4g'):
        # code inspired by Indian Pythonista (https://www.youtube.com/channel/UCkUq-s6z57uJFUFBvZIVTyg)
        # to get your own api_key watch https://www.youtube.com/watch?v=-QMg39gK624
        api_key = '****'
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel_list = youtube.channels().list(id=channel_id, part='contentDetails').execute()
        playlist_id = channel_list['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        videos = []
        next_page_token = None

        while True:
            response = youtube.playlistItems().list(playlistId=playlist_id,
                                                    part='snippet',
                                                    maxResults=50,
                                                    pageToken=next_page_token).execute()
            videos += response['items']
            next_page_token = response.get('nextPageToken')

            if next_page_token is None:
                break

        youtube_videos = []
        for video in videos:
            video_info = video['snippet']
            title = video_info['title'].replace('Kaifeck - ', '')
            video_id = video_info['resourceId']['videoId']
            upload_datetime = timezone.make_aware(datetime.strptime(video_info['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"))

            y = YouTubeVideo.objects.filter(video_id=video_id)
            if not y.exists():
                y = YouTubeVideo.objects.create(
                    title=title,
                    video_id=video_id,
                    upload_datetime=upload_datetime,
                    show_on_website=False
                )
                youtube_videos.append(y)
            else:
                youtube_videos.append(y.first())

        return youtube_videos
