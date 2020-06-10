from django.urls import path, re_path

from website import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^news/?$', views.news_list, name='news_list'),
    re_path(r'^news/(?P<pk>[0-9]+)/?$', views.news_detail, name='news_detail'),
    re_path(r'^shows/?$', views.shows_list, name='shows_list'),
    re_path(r'^shows/(?P<pk>[0-9]+)/?$', views.shows_detail, name='shows_detail'),
    path('send_mail/', views.mail, name='send_mail')
]
