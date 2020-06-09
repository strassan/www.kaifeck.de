from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

from smtplib import SMTPException

from .models import YouTubeVideo, News, Gig


def index(request):
    videos = YouTubeVideo.objects.filter(show_on_website=True).order_by('-upload_datetime')
    gigs = [gig for gig in Gig.objects.all() if gig.is_open]
    news = [n for n in News.objects.all() if n.is_open]
    context = {
        'videos': videos,
        'news': news,
        'gigs': gigs
    }
    return render(request, "website/index.html", context)


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
            context = {
                'success': False, 'smtp_error': '{errno:d}: {str}'.format(
                    errno=getattr(err, 'smtp_code', -1),
                    str=getattr(err, 'smtp_error', 'ignore').decode("utf-8")
                )
            }
    else:
        context = {'success': False, 'smtp_error': 'fail'}
    return render(request, 'website/send_mail.html', context)
