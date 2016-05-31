from django.db import models
from django.conf import settings

class Portfolio(models.Model):
    owner=models.ForeignKey(Profile)
    # pics_folder_url = "url"


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    contact_mail=models.EmailField()
    short_description=models.CharField(max_length=1000)