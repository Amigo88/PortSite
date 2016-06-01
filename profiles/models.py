from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    contact_mail = models.EmailField()
    short_description = models.CharField(max_length=1000)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return  reverse("profiles:detail", args=(self.pk,))

class Photo(models.Model):
    profile = models.ForeignKey(Profile)
    image = models.ImageField(upload_to="photos/")
