from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
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


class UIMixin:
    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['all_profiles'] = models.Profile.objects.all()
        return d

        # all_profiles = models.Profile.objects.all()


class ListProfilesView(UIMixin, LoggedInMixin, ListView):
    page_title = "Portfolios"
    model = models.Profile
    # template_name = "profiles\profile_list.html"


class CreateProfileView(UIMixin, LoggedInMixin, CreateView):
    page_title = "Create New Profile"
    model = models.Profile
    form_class = forms.ProfileForm

    success_url = reverse_lazy('profiles:list')

    def dispatch(self, request, pk, *args, **kwargs):
        self.user = get_object_or_404(models.User, id=pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.user
        form.instance.first_name = self.user.first_name
        form.instance.last_name = self.user.last_name
        form.instance.contact_mail = self.user.email
        resp = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Profile added")
        return resp

        # template_name = "profiles\profile_form.html"


class ProfileDetailView(UIMixin, LoggedInMixin, DetailView):
    page_title = "Portfolio"
    model = models.Profile

    # def get_queryset(self):
    #     return super().get_queryset().filter(profile__user=self.request.user)
    # template_name = "profiles\profile_list.html"


class ProjectDetailView(UIMixin, LoggedInMixin, DetailView):
    page_title = "Project"
    model = models.Project

    def dispatch(self, request, profile_id, *args, **kwargs):
        self.profile = get_object_or_404(models.Profile, id=profile_id)
        return super().dispatch(request, *args, **kwargs)

        def get_queryset(self):
            return super().get_queryset().filter(project=self.project)


class AddWorkView(UIMixin, LoggedInMixin, CreateView):
    page_title = "Add Work"
    model = models.Photo
    form_class = forms.PhotoForm

    def dispatch(self, request, project_id, *args, **kwargs):
        self.project = get_object_or_404(models.Project, id=project_id)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(project=self.project)

    def get_success_url(self):
        return self.project.get_absolute_url()

    def form_valid(self, form):
        form.instance.project = self.project
        resp = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Workd added")
        return resp


class AddProjectView(UIMixin, LoggedInMixin, CreateView):
    page_title = "Add Project"
    model = models.Project
    form_class = forms.ProjectForm

    def get(self, request, profile_id, *args, **kwargs):
        self.profile = get_object_or_404(models.Profile, id=profile_id)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(profile=self.profile)

    def get_success_url(self):
        return self.object.profile.get_absolute_url()

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        resp = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Project added")
        return resp


class DeleteWorkView(UIMixin, LoggedInMixin, DeleteView):
    page_title = "Delete Work"
    model = models.Photo
    form_class = forms.PhotoForm

    def dispatch(self, request, profile_id, *args, **kwargs):
        self.project = get_object_or_404(models.Profile, id=profile_id)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(DeleteWorkView, self).get_object()
        if obj.project.profile.user != self.request.user:
            raise Http404()
        return obj

    def get_success_url(self):
        return self.object.project.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().image.delete()
        except IOError:
            pass
        resp = super().delete(request, *args, **kwargs)
        messages.info(request, "Photo deleted")
        return resp


class DeleteProjectView(UIMixin, LoggedInMixin, DeleteView):
    page_title = "Delete Project"
    model = models.Project
    form_class = forms.ProjectForm

    def dispatch(self, request, profile_id, *args, **kwargs):
        self.profile= get_object_or_404(models.Profile, id=profile_id)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(DeleteProjectView, self).get_object()
        if obj.profile.user != self.request.user:
            raise Http404()
        return obj

    def get_success_url(self):
        return self.object.profile.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        try:
            for photo in self.get_object().photos.all():
                photo.image.delete()
        except IOError:
            pass
        resp = super().delete(request, *args, **kwargs)
        messages.info(request, "Project deleted")
        return resp


class SignupView(FormView):
    page_title = "Signup"
    form_class = forms.SignupForm
    template_name = "signup.html"
    success_url = reverse_lazy('profiles:list')

    def form_valid(self, form):
        if form.cleaned_data['password'] != form.cleaned_data.pop('password_validation'):
            form.add_error(None, "Passwords do not match")
            return self.form_invalid(form)

        user = User.objects.create_user(**form.cleaned_data)
        user = authenticate(**form.cleaned_data)
        login(self.request, user)

        if self.request.GET.get('from'):
            return redirect(self.request.GET['from'])
        return redirect('profiles:list')
