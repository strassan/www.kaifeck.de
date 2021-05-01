from django.db import models
from django.utils import timezone


class Link(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=256)
    alt_url = models.CharField(
        max_length=256,
        verbose_name="Alternative Url",
        help_text="Provide an alternative url, if original url does not use http or https protocol",
        null=True, blank=True
    )
    image = models.ImageField(
        help_text="For best result, always upload images with 1:1 aspect ratio",
        upload_to='links'
    )
    open_date = models.DateField(
        help_text="The first day on which the link will be visible on the linkpage",
        null=True, blank=True
    )
    close_date = models.DateField(
        help_text="The last day on which the link will be visible on the linkpage",
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
    def is_open(self):
        if self.close_date is None and self.open_date is None:
            return True  # it is always open
        elif self.close_date is None and self.open_date is not None:
            return timezone.now().date() >= self.open_date  # it is only open once the open date was reached
        elif self.close_date is not None and self.open_date is None:
            return timezone.now().date() <= self.close_date  # it is only open until the close date was reached
        else:  # both close and open date exist
            return self.open_date <= timezone.now().date() <= self.close_date  # it is open from open until close date

    @property
    def is_closed(self):
        return not self.is_open
