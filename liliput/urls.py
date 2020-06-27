from django.urls import path

from liliput import views

app_name = 'liliput'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:short_url>', views.open_short_link, name='open_short_link')
]
