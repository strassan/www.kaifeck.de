from django.contrib import admin
from liliput.models import ShortLink


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'modified_at', 'number_of_requests',)
