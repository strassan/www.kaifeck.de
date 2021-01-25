from django.contrib import admin


def verify_selected_short_links(modeladmin, request, queryset):
    queryset.update(verified=True)


def unverify_selected_short_links(modeladmin, request, queryset):
    queryset.update(verified=False)


# for ShortLinks
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ['short_url', 'verified', 'close_date']
    ordering = ['-verified', '-modified_at']
    actions = [verify_selected_short_links, unverify_selected_short_links]
    readonly_fields = ('created_at', 'modified_at', 'number_of_requests',)
