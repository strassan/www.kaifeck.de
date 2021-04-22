from django.contrib import admin


class LinkAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'modified_at',)
