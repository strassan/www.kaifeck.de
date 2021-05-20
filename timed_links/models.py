from django.db import models
from django.utils import timezone
from django.urls import reverse

import string
import random

from kaifeck.settings import ALLOWED_HOSTS


class TimedLink(models.Model):
    path = models.CharField(max_length=32, null=True, blank=True, unique=True,
                            help_text="The part of the URL after the /")

    open_time = models.DateTimeField(help_text="The time at which the link should be opened.")
    close_time = models.DateTimeField(help_text="The time at which the link should be closed.")
    redirect_url = models.CharField(max_length=256, help_text="The URL the link will redirect to, while it is open.")

    message_when_too_early = models.TextField(
        help_text="The message to be shown, when the link has been opened before the open time was reached."
    )
    message_when_too_late = models.TextField(
        help_text="The message to be shown, when the link has been opened after the close time was reached."
    )

    # TODO: add missing fields

    number_of_requests = models.IntegerField(editable=False)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField(editable=False)

    def save(self, modify=True, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
            self.number_of_requests = 0
            self.modified_at = timezone.now()
        if not self.short_url:
            chars = string.digits + string.ascii_letters + "$-_+!*"
            random_url = ''
            loop = True
            while loop:
                random_url = ''.join(random.choice(chars) for i in range(6))
                qs = ShortLink.objects.filter(short_url=random_url)
                loop = qs.exists()
            self.short_url = random_url
        if modify:
            self.modified_at = timezone.now()
        return super(TimedLink, self).save(*args, **kwargs)

    def __str__(self):
        return self.short_url

    def get_short_url(self):
        if len(ALLOWED_HOSTS) > 0:
            return ALLOWED_HOSTS[0] + reverse('liliput:index') + str(self.short_url)
        else:
            return reverse('liliput:index') + str(self.short_url)

    def get_redirect_url(self):
        if self.redirect_url[0:7] == 'http://' or self.redirect_url[0:8] == 'https://':
            return self.redirect_url
        else:
            return 'http://' + self.redirect_url

    @property
    def is_closed(self):
        if self.close_date is not None:
            return timezone.now().date() > self.close_date
        else:
            False

    @property
    def is_open(self):
        return not self.is_closed
