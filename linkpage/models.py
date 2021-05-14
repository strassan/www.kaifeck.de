import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone

from PIL import Image


THUMB_SIZE = (250, 250)


class LinkFolder(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
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
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')
        return super(LinkFolder, self).save(*args, **kwargs)

    def make_thumbnail(self):
        image = Image.open(self.image)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.image.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

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


class Link(LinkFolder):
    url = models.CharField(max_length=256)
    alt_url = models.CharField(
        max_length=256,
        verbose_name="Alternative Url",
        help_text="Provide an alternative url, if original url does not use http or https protocol",
        null=True, blank=True
    )
    parent_folder = models.ForeignKey(LinkFolder, models.CASCADE, null=True, blank=True, related_name='+')
