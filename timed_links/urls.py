from django.urls import path

from timed_links import views

app_name = 'timed_links'

urlpatterns = [
    path('<str:path>', views.open_link, name='open_link')
]
