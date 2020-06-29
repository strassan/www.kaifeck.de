from django.shortcuts import render, redirect
from django.http import Http404

from liliput.models import ShortLink
from liliput.forms import ShortLinkForm


def index(request, context=None):
    if context is None:
        context = dict()
    form = ShortLinkForm(data=request.POST if request.POST else None)
    if request.POST and form.is_valid():
        instance = form.save()
        context['new_short_url'] = instance.short_url
        context['form'] = ShortLinkForm()
    else:
        context['form'] = form
    return render(request, "liliput/index.html", context)


def open_short_link(request, short_url):
    qs = ShortLink.objects.filter(short_url=short_url)
    if qs.exists():
        if qs.first().is_open:
            return redirect(qs.first().get_redirect_url())
        else:
            return index(request, context={'message': 'This short link expired.'})
    else:
        return index(request, context={'message': 'This short link does not exist.'})
