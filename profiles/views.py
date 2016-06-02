from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import FormView, CreateView, ListView, DeleteView
from django.views.generic.detail import DetailView

from . import forms, models
from django.views.generic import View


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('profiles:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if user is not None and user.is_active:
            login(self.request, user)
            if self.request.GET.get('from'):
                return redirect(
                    self.request.GET['from'])  # SECURITY: check path
            return redirect('profiles:list')

        form.add_error(None, "Invalid user name or password")
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class LoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            url = reverse("login") + "?from=" + escape_uri_path(request.path)
            return redirect(url)
        return super().dispatch(request, *args, **kwargs)


class ListProfilesView(LoggedInMixin, ListView):
    page_title = "Profiles"
    model = models.Profile
    # template_name = "profiles\profile_list.html"


class CreateProfileView(LoggedInMixin, CreateView):
    page_title = "Create New Profile"
    model = models.Profile
    form_class = forms.ProfileForm

    success_url = reverse_lazy('profiles:list')

    # template_name = "profiles\profile_form.html"


class ProfileDetailView(LoggedInMixin, DetailView):
    page_title = "Portfolio"
    model = models.Profile

    # def get_queryset(self):
    #     return super().get_queryset().filter(profile__user=self.request.user)
    # template_name = "profiles\profile_list.html"


class AddWorkView(LoggedInMixin, CreateView):
    page_title = "Add Work"
    model = models.Photo
    form_class = forms.PhotoForm

    success_url = reverse_lazy('profiles:list')

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class DeleteWorkView(LoggedInMixin, DeleteView):
    page_title = "Delete Work"
    model = models.Photo
    form_class = forms.PhotoForm

    def get_object(self, queryset=None):
        obj = super(DeleteWorkView, self).get_object()
        if obj.profile.user != self.request.user:
            raise Http404()
        return obj

    def get_success_url(self):
        return self.object.profile.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().image.delete()
        except IOError:
            pass
        resp = super().delete(request, *args, **kwargs)
        messages.info(request, "Photo deleted")
        return resp


