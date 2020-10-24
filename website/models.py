from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    close_date = models.DateField(help_text="The last day on which the post is visible on the homepage")
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_closed(self):
        return timezone.now().date() > self.close_date

    @property
    def is_open(self):
        return not self.is_closed


class Gig(Post):
    gig_start_date = models.DateField()
    gig_start_time = models.TimeField(blank=True, null=True)
    gig_end_date = models.DateField(blank=True, null=True)
    gig_end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=64)
    google_maps_link = models.CharField(max_length=256, blank=True)
    ticket_link = models.CharField(max_length=256, blank=True)


class News(Post):
    short_description = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class YouTubeVideo(models.Model):
    title = models.CharField(max_length=64)
    video_id = models.CharField(max_length=64)
    upload_datetime = models.DateTimeField()
    show_on_website = models.BooleanField()

    class Meta:
        verbose_name = 'YouTube video'
        verbose_name_plural = 'YouTube videos'

    def __str__(self):
        return self.title

    def get_embed_link(self):
        return 'https://www.youtube.com/embed/' + self.video_id

    def get_video_link(self):
        return 'https://www.youtube.com/watch?v=' + self.video_id
