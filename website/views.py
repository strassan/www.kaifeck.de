from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import Library
from django.conf import settings
from django.utils.html import strip_tags

from datetime import timedelta

from smtplib import SMTPException
from socket import gaierror

from .models import YouTubeVideo, News, Gig


register = Library()


@register.filter
def substract(value, arg):
    return value - arg


def index(request):
    videos = YouTubeVideo.objects.filter(show_on_website=True).order_by('-upload_datetime')
    gigs = [gig for gig in Gig.objects.all().order_by('-gig_start_date') if gig.is_open]
    news = [n for n in News.objects.all().order_by('-created_at') if n.is_open]
    context = {
        'videos': videos,
        'news': news,
        'gigs': gigs,
        'timedelta': timedelta(minutes=5)
    }
    return render(request, "website/index.html", context)


def news_list(request):
    news = News.objects.all().order_by('-created_at')
    context = {
        'news': news
    }
    return render(request, "website/news_list.html", context)


def news_detail(request, pk):
    n = News.objects.get(pk=pk)
    context = {
        'n': n
    }
    return render(request, "website/news_detail.html", context)


def shows_list(request):
    gigs = Gig.objects.order_by('-gig_start_date')
    upcoming_gigs = [gig for gig in gigs if gig.is_open]
    past_gigs = [gig for gig in gigs if gig.is_closed]
    context = {
        'gigs': upcoming_gigs + past_gigs,
        'num_upcoming': len(upcoming_gigs)
    }
    return render(request, "website/shows_list.html", context)


def shows_detail(request, pk):
    gig = Gig.objects.get(pk=pk)
    context = {
        'gig': gig
    }
    return render(request, "website/shows_detail.html", context)


def mail(request):
    if request.POST:
        mail_context = {
            'sender_email': request.POST.get('sender_email'),
            'sender_message': request.POST.get('sender_message')
        }
        sender_html = render_to_string('website/mails/sender_mail.j2', context=mail_context)
        kaifeck_html = render_to_string('website/mails/kaifeck_mail.j2', context=mail_context)
        try:
            send_mail(
                subject='Your message to Kaifeck',
                message=strip_tags(sender_html),
                from_email=settings.EMAIL_SENDER,
                recipient_list=[mail_context['sender_email']],
                html_message=sender_html.replace('\n', '<br/>'),
                fail_silently=False
            )
            send_mail(
                subject='New message on kaifeck.de',
                message=strip_tags(kaifeck_html),
                from_email=settings.EMAIL_SENDER,
                recipient_list=[settings.EMAIL_HOST_USER],
                html_message=kaifeck_html.replace('\n', '<br/>'),
                fail_silently=False
            )
            context = {'success': True, 'smtp_error': str()}
        except SMTPException as err:
            # usually sth like "Error 535: Authentication Failed"
            # fix: set correct EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py
            context = {
                'success': False, 'smtp_error': '{errno:d}: {str}'.format(
                    errno=err.smtp_code,
                    str=err.smtp_error.decode("utf-8")
                )
            }
        except gaierror as err:
            # usually sth like "Error 11001: getaddrinfo failed"
            # fix: set correct EMAIL_HOST in settings.py
            context = {
                'success': False, 'smtp_error': '{errno:d}: {str}'.format(
                    errno=err.errno, str=err.strerror
                )
            }
            print(dir(err))
    else:
        context = {'success': False, 'smtp_error': 'fail'}
    return render(request, 'website/send_mail.html', context)


def legal_notice(request):
    context = {
        'legal_notice': settings.LEGAL_NOTICE
    }
    return render(request, 'website/legal_notice.html', context)
