from django import forms
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = [
            'user',
            'first_name',
            'last_name',
            'contact_mail',
            'short_description'
        ]

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = [
            'image',
        ]