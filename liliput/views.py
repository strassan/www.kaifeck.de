from django.shortcuts import render, redirect
from django.http import Http404

from liliput.models import ShortLink
from liliput.forms import ShortLinkForm


def index(request):
    form = ShortLinkForm(data=request.POST if request.POST else None)
    context = {
        'form': form
    }
    if request.POST and form.is_valid():
        form.save()
    return render(request, "liliput/index.html", context)


def open_short_link(request, short_url):
    qs = ShortLink.objects.filter(short_url=short_url)
    if qs.exists():
        if qs.first().is_open:
            return redirect(qs.first().redirect_url)
        else:
            raise Http404('Short link expired.')
    else:
        raise Http404('Short link does not exist.')
