from django.db import models
from django.utils import timezone


class TimedLink(models.Model):
    path = models.CharField(max_length=32, null=True, blank=True, unique=True,
                            help_text="The part of the URL after the /")

    open_time = models.DateTimeField(help_text="The time at which the link should be opened.")
    close_time = models.DateTimeField(help_text="The time at which the link should be closed.")
    redirect_url = models.CharField(max_length=256, help_text="The URL the link will redirect to, while it is open.")

    message_when_too_early = models.TextField(
        help_text="The message to be shown, when the link has been opened before the open time was reached."
    )
    message_on_homepage = models.TextField(
        help_text="The message to be shown on the homepage while the link is open."
    )
    message_when_too_late = models.TextField(
        help_text="The message to be shown, when the link has been opened after the close time was reached."
    )

    button_text = models.CharField(max_length=128, help_text="The text on the button")

    number_of_requests = models.IntegerField(editable=False)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
            self.number_of_requests = 0
        self.modified_at = timezone.now()
        return super(TimedLink, self).save(*args, **kwargs)

    def __str__(self):
        return self.path

    def get_redirect_url(self):
        if self.redirect_url[0:7] == 'http://' or self.redirect_url[0:8] == 'https://':
            return self.redirect_url
        else:
            return 'http://' + self.redirect_url

    @property
    def is_open(self):
        return self.open_time < timezone.now() < self.close_time

    @property
    def is_closed(self):
        return not self.is_open

    @property
    def is_too_early(self):
        return timezone.now() < self.open_time

    @property
    def is_too_late(self):
        return self.close_time < timezone.now()
