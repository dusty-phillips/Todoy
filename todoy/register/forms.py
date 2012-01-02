from django import forms
from mongoengine.django.auth import User


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(max_length=72)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise forms.ValidationError("The passwords do not match")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        else:
            raise forms.ValidationError("The user %s already exists" % username)

