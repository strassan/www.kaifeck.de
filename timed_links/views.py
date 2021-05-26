from django.shortcuts import render, redirect

from .models import TimedLink


def open_link(request, path):
    qs = TimedLink.objects.filter(path=path)
    if qs.exists():
        timed_link = qs.first()
        timed_link.number_of_requests += 1
        timed_link.save(modify=False)
        if timed_link.is_open:
            return redirect(timed_link.get_redirect_url())
        else:
            context = {
                'timed_link': timed_link,
                'is_too_early': timed_link.is_too_early,
                'timed_link_redirect': timed_link.get_redirect_url(),
            }
            return render(request, "timed_links/index.html", context)
    else:
        return redirect(path + '/')
