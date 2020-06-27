from django import forms

from liliput.models import ShortLink


class ShortLinkForm(forms.ModelForm):
    class Meta:
        model = ShortLink
        fields = ['short_url', 'redirect_url', 'close_date']
