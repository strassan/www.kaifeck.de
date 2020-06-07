from django.contrib import admin
from django.urls import path

from website.views import index, mail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('send_mail', mail, name='send_mail')
]
