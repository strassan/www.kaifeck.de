from django.urls import path, re_path
from django.conf.urls.static import static

from kaifeck import settings
from website import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('shows/', views.shows_list, name='shows_list'),
    path('shows/<int:pk>/', views.shows_detail, name='shows_detail'),
    path('send_mail/', views.mail, name='send_mail'),
    path('legal_notice/', views.legal_notice, name='legal_notice'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
