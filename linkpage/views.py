from django.shortcuts import render
from django.db.models import Exists, OuterRef

from .models import LinkFolder, Link


def index(request):
    link_folders = LinkFolder.objects.filter(~Exists(Link.objects.filter(linkfolder_ptr_id=OuterRef('pk'))))\
        .order_by('-modified_at')
    link_folders = [lf for lf in link_folders if lf.is_open]

    child_links = {}
    for lf in link_folders:
        child_links[lf.pk] = Link.objects.filter(parent_folder=lf).order_by('-modified_at')

    links_without_parent_folder = Link.objects.all().order_by('-modified_at')
    links_without_parent_folder = [l for l in links_without_parent_folder if l.is_open and l.parent_folder is None]

    context = {
        'link_folders': link_folders,
        'child_links': child_links,
        'links': links_without_parent_folder,
    }

    return render(request, "linkpage/index.html", context)
