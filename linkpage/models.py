from django.db import models
from django.utils import timezone


class Link(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=256)
    image = models.ImageField(
        help_text="For best result, always upload images with 1:1 aspect ratio",
        upload_to='links'
    )
    close_date = models.DateField(
        help_text="The last day on which the link is visible on the linkpage",
        null=True, blank=True
    )
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Link, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_closed(self):
        if self.close_date is None:
            return False
        else:
            return timezone.now().date() > self.close_date

    @property
    def is_open(self):
        return not self.is_closed
