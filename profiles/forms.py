from django import forms
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = [
            # 'user',
            # 'first_name',
            # 'last_name',
            # 'contact_mail',

            'short_description'
        ]


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = [
            'image',
        ]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'name',
            'short_description',
        ]


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=300)
    last_name = forms.CharField(max_length=300)
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())
    password_validation = forms.CharField(max_length=300, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=300)
