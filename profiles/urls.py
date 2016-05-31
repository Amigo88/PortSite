from django.conf.urls import url

from . import views

app_name = "profiles"
urlpatterns = [
    url(r'^$', views.ListProfilesView.as_view(), name="list"),
    url(r'^add/$', views.CreateProfileView.as_view(), name="create"),
]