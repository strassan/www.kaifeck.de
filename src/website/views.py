from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

from smtplib import SMTPException

from .models import Post, YouTubeVideo
from .forms import EmailForm


def index(request):
    videos = YouTubeVideo.objects.filter(show_on_website=True).order_by('-upload_datetime')
    context = {
        'videos': videos,
        'form': EmailForm()
    }
    if request.POST:
        form = EmailForm(data=request.POST)
        if form.is_valid():
            mail_context = {
                'sender_email': form.cleaned_data.get('sender_email'),
                'sender_message': form.cleaned_data.get('sender_message')
            }
            sender_html = render_to_string('mails/sender_mail.j2', context=mail_context)
            kaifeck_html = render_to_string('mails/kaifeck_mail.j2', context=mail_context)
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
            except SMTPException as err:
                context['error'] = err
        else:
            context['error'] = 'Invalid Email address'

    return render(request, "index.html", context)
