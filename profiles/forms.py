from django import forms
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())

class ProfileForm(forms.ModelForm):
    class Meta:
        fields = [
            'First name',
            'Last name',
            'Contact Email',
            'Short Description'
        ]