from django.contrib import admin


# for TimedLinks
class TimedLinkAdmin(admin.ModelAdmin):
    list_display = ['path', 'redirect_url', 'open_time', 'close_time', 'number_of_requests']
    ordering = ['-modified_at']
    readonly_fields = ('created_at', 'modified_at', 'number_of_requests',)
