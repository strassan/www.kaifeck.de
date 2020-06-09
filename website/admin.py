from django.contrib import admin, messages
from django.urls import path
from django.conf import settings
from django.shortcuts import HttpResponseRedirect
from django.utils import timezone
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as GoogleHttpError
import json

from .models import YouTubeVideo, Gig, News


def make_visible_on_website(modeladmin, request, queryset):
    queryset.update(show_on_website=True)


def make_invisible_on_website(modeladmin, request, queryset):
    queryset.update(show_on_website=False)


@admin.register(YouTubeVideo)
class YouTubeAdmin(admin.ModelAdmin):
    list_display = ['title', 'show_on_website']
    ordering = ['-show_on_website', '-upload_datetime']
    actions = [make_invisible_on_website, make_visible_on_website]
    change_list_template = 'entities/youtube_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('get_uploads/', self.get_uploads)
        ]
        return my_urls + urls

    def get_uploads(self, request):
        # code inspired by Indian Pythonista (https://www.youtube.com/channel/UCkUq-s6z57uJFUFBvZIVTyg)
        # to get your own api_key watch https://www.youtube.com/watch?v=-QMg39gK624
        channel_id = 'UCU5yJUgbF9E2LxDLS-voY4g'
        try:
            youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        except GoogleHttpError as err:
            self.message_user(
                request,
                json.loads(err.content.decode('utf-8'))['error']['message'],
                level=messages.ERROR)
            return HttpResponseRedirect('../')
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

        num_new_videos = 0
        for video in videos:
            video_info = video['snippet']
            title = video_info['title'].replace('Kaifeck - ', '')
            video_id = video_info['resourceId']['videoId']
            upload_datetime = timezone.make_aware(datetime.strptime(video_info['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"))

            y = self.model.objects.filter(video_id=video_id)
            if not y.exists():
                self.model.objects.create(
                    title=title,
                    video_id=video_id,
                    upload_datetime=upload_datetime,
                    show_on_website=False
                )
                num_new_videos += 1

        if num_new_videos == 0:
            self.message_user(request, 'Videos up to date. No new uploads found.')
        else:
            self.message_user(request, 'Videos have been updated.')
        return HttpResponseRedirect('../')


@admin.register(Gig, News)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'modified_at',)
