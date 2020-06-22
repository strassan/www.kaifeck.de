from django.shortcuts import render, redirect
from django.http import Http404

from liliput.models import ShortLink


def open_short_link(request, short_url):
    qs = ShortLink.objects.filter(short_url=short_url)
    if qs.exists():
        if qs.first().is_open:
            return redirect(qs.first().redirect_url)
        else:
            raise Http404('Short link expired.')
    else:
        raise Http404('Short link does not exist.')
