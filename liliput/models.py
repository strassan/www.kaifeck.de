from django.db import models
from django.utils import timezone
from django.urls import reverse

import string
import random

from kaifeck.settings import ALLOWED_HOSTS


class ShortLink(models.Model):
    short_url = models.CharField(max_length=32, null=True, blank=True, unique=True)
    redirect_url = models.CharField(max_length=256)
    close_date = models.DateField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    number_of_requests = models.IntegerField(editable=False)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField(editable=False)

    def save(self, modify=True, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
            self.number_of_requests = 0
            self.modified_at = timezone.now()
        if not self.short_url:
            chars = string.digits + string.ascii_letters
            random_url = ''
            loop = True
            while loop:
                random_url = ''.join(random.choice(chars) for i in range(6))
                qs = ShortLink.objects.filter(short_url=random_url)
                loop = qs.exists()
            self.short_url = random_url
        if modify:
            self.modified_at = timezone.now()
        return super(ShortLink, self).save(*args, **kwargs)

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
