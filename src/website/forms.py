from django import forms


class EmailForm(forms.Form):
    sender_email = forms.EmailField()
    sender_message = forms.TextInput()
