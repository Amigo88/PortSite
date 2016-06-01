from django.conf.urls import url

from . import views

app_name = "profiles"
urlpatterns = [
    url(r'^$', views.ListProfilesView.as_view(), name="list"),
    url(r'^add_profile/$', views.CreateProfileView.as_view(), name="create"),
    url(r'^add_work/$', views.AddWorkView.as_view(), name="add"),
    url(r'^(?P<pk>\d+)/$', views.ProfileDetailView.as_view(), name="profile"),
]