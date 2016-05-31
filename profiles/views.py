from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic import FormView
from . import forms
from django.views.generic import View


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = "login.html"


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")
