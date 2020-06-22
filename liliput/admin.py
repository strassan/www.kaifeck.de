from django.contrib import admin
from liliput.models import ShortLink

# Register your models here.


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'modified_at',)
