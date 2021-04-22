from django.shortcuts import render

from .models import Link


def index(request):
    links = Link.objects.all().order_by('-modified_at')
    links = [l for l in links if l.is_open]
    context = {
        'links': links
    }
    return render(request, "linkpage/index.html", context)
