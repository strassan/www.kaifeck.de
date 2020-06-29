from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


from django.conf import settings


from liliput.models import ShortLink
from liliput.forms import ShortLinkForm


def index(request, context=None):
    if context is None:
        context = dict()
    form = ShortLinkForm(data=request.POST if request.POST else None)
    if request.POST and form.is_valid():
        instance = form.save()
        context['new_short_url'] = instance.short_url
        context['form'] = ShortLinkForm()
        mail_context = {
            'short_link': instance.get_short_url(),
            'redirect_link': instance.get_redirect_url(),
        }
        if instance.close_date is not None:
            mail_context['close_date'] = instance.close_date
        mail_html = render_to_string('liliput/mails/new_short_link_created.j2', context=mail_context)
        send_mail(
            subject='[Liliput] New short link created',
            message=strip_tags(mail_html),
            from_email=settings.EMAIL_SENDER,
            recipient_list=['liliput@kaifeck.de'],
            html_message=mail_html.replace('\n', '<br/>'),
            fail_silently=True
        )
    else:
        context['form'] = form
    return render(request, "liliput/index.html", context)


def open_short_link(request, short_url):
    qs = ShortLink.objects.filter(short_url=short_url)
    if qs.exists():
        if qs.first().is_open:
            return redirect(qs.first().get_redirect_url())
        else:
            return index(request, context={'message': 'This short link expired.'})
    else:
        return index(request, context={'message': 'This short link does not exist.'})
