from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    contact_mail = models.EmailField()
    short_description = models.CharField(max_length=1000)

class Photo(models.Model):
    profile = models.ForeignKey(Profile)
    image = models.ImageField(upload_to="photos/")
