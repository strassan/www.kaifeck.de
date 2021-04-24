from django.contrib import admin


class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'open_date', 'close_date']
    ordering = ['-modified_at']
    readonly_fields = ('created_at', 'modified_at',)
