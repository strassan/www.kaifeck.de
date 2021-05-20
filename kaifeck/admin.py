from django.contrib.admin import *

from website.models import YouTubeVideo, Gig, News
from website.admin import YouTubeAdmin, PostAdmin
from liliput.models import ShortLink
from liliput.admin import ShortLinkAdmin
from linkpage.models import LinkFolder, Link
from linkpage.admin import LinkFolderAdmin, LinkAdmin
from timed_links.models import TimedLink
from timed_links.admin import TimedLinkAdmin


class MyAdminSite(AdminSite):
    site_title = 'Kaifeck admin'
    site_header = 'Kaifeck administration'

    login_template = "login.html"

    def __init__(self, *args, **kwargs):
        super(MyAdminSite, self).__init__(*args, **kwargs)
        self._registry.update(site._registry)


site = MyAdminSite()

site.register(YouTubeVideo, YouTubeAdmin)
site.register(Gig, PostAdmin)
site.register(News, PostAdmin)
site.register(ShortLink, ShortLinkAdmin)
site.register(LinkFolder, LinkFolderAdmin)
site.register(Link, LinkAdmin)
site.register(TimedLink, TimedLinkAdmin)
