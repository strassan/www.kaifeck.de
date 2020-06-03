from django.shortcuts import render

from .models import Post, YouTubeVideo


def index(request):
    videos = YouTubeVideo.objects.filter(show_on_website=True).order_by('-upload_datetime')
    context = {
        'videos': videos
    }
    return render(request, "index.html", context)
