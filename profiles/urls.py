from django.conf.urls import url

from . import views

app_name = "profiles"
urlpatterns = [
    url(r'^$', views.ListProfilesView.as_view(), name="list"),
    url(r'^add_profile/(?P<pk>\d+)/$', views.CreateProfileView.as_view(), name="create"),
    url(r'^profile/(?P<profile_id>\d+)/projects/(?P<project_id>\d+)/add_work/$', views.AddWorkView.as_view(), name="add_work"),
    url(r'^profile/(?P<profile_id>\d+)/add_project/$', views.AddProjectView.as_view(), name="add_project"),
    url(r'^profile/(?P<profile_id>\d+)/delete_work/(?P<pk>\d+)/$', views.DeleteWorkView.as_view(), name="delete"),
    url(r'^profile/(?P<profile_id>\d+)/delete_project/(?P<pk>\d+)/$', views.DeleteProjectView.as_view(), name="project_delete"),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileDetailView.as_view(), name="detail"),
    url(r'^profile/(?P<profile_id>\d+)/projects/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name="project_detail"),
    url(r'^signup/$', views.SignupView.as_view(), name="signup"),
]