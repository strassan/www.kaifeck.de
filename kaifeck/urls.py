from django.urls import path, include
from kaifeck.settings import ADMIN_URL
from .admin import site

urlpatterns = [
    path(ADMIN_URL, site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('', include('website.urls', namespace='website')),
    path('l/', include('liliput.urls', namespace='liliput')),
    path('links/', include('linkpage.urls', namespace='linkpage')),
    path('', include('timed_links.urls', namespace='timed_links')),  # must always be the last path in the list
]
