from django import forms

from liliput.models import ShortLink


class ShortLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShortLinkForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'col-8 col-lg-4 mx-auto form-control'
            visible.label_class = 'col-12 col-lg-4 my-auto'
        self.fields['short_url'].widget.attrs['placeholder'] = 'short URL (leave empty for random)'
        self.fields['redirect_url'].widget.attrs['placeholder'] = 'http://example.com'

    class Meta:
        model = ShortLink
        fields = ['short_url', 'redirect_url', 'close_date']
        labels = {
            'short_url': '(optional) kaifeck.de/l/...',
            'redirect_url': 'Redirect to:',
            'close_date': '(optional) Expires on:'
        }
        widgets = {
            'close_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
