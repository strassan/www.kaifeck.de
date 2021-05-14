from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Exists, OuterRef
from django import forms

from .models import LinkFolder, Link


def folder_form_factory():
    """ This function filters the dropdown menu in the LinkAdmin to only show Folders (not Links) """
    class TagForm(forms.ModelForm):
        parent_folder = forms.ModelChoiceField(
            queryset=LinkFolder.objects.filter(~Exists(Link.objects.filter(linkfolder_ptr_id=OuterRef('pk')))),
            required=False
        )
    return TagForm


class FolderFilter(SimpleListFilter):
    """ This class filters the list of LinkFolders in the LinkFolderAdmin to only show Folders that are not Links. """

    title = 'Type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            (None, 'Folder'),
            ('link', 'Link'),
            ('all', 'All'),
        )

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': changelist.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() in ('link',):
            return queryset.filter(Exists(Link.objects.filter(linkfolder_ptr_id=OuterRef('pk'))))
        elif self.value() is None:
            return queryset.filter(~Exists(Link.objects.filter(linkfolder_ptr_id=OuterRef('pk'))))
        else:
            pass


class LinkFolderAdmin(admin.ModelAdmin):
    list_filter = [FolderFilter]
    list_display = ['title', 'open_date', 'close_date']
    ordering = ['-modified_at']
    readonly_fields = ('created_at', 'modified_at',)


class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'open_date', 'close_date', 'parent_folder']
    ordering = ['-parent_folder', '-modified_at']
    readonly_fields = ('created_at', 'modified_at',)

    # TODO: the query makes the "+" symbol to add a new LinkFolder disappear next to the dropdown menu.
    #   Would be nice to find a way to make it reappear.
    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['form'] = folder_form_factory()
        return super(LinkAdmin, self).get_form(request, obj, change, **kwargs)
