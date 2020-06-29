from django.db import models
from django.utils import timezone


class ShortLink(models.Model):
    short_url = models.CharField(max_length=32, unique=True)
    redirect_url = models.CharField(max_length=256)
    close_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(ShortLink, self).save(*args, **kwargs)

    def __str__(self):
        return self.short_url

    def get_short_url(self):
        return 'kaifeck.de/l/' + str(self.short_url)

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
