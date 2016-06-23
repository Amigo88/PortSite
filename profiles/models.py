from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User


#
# class Owner(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         related_name="owners",
#     )
#
#     def __str__(self):
#         return "{} {}".format(self.user.first_name, self.user.last_name)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    contact_mail = models.EmailField()
    short_description = models.CharField(max_length=1000)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse("profiles:detail", args=(self.pk,))


class Project(models.Model):
    profile = models.ForeignKey(Profile, related_name="projects")
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=500)

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse("profiles:project_detail", args=(self.profile_id, self.pk))


class Photo(models.Model):
    project = models.ForeignKey(Project, related_name="photos")
    image = models.ImageField(upload_to="photos/")


class ProjectLike(models.Model):
    project = models.ForeignKey(Project, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="likes")

    class Meta:
        unique_together = (
            ('project', 'user'),
        )