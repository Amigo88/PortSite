from django.contrib.auth.models import User
from django.test import TestCase
from . import models


class ProfilesTestCase(TestCase):
    def test_portfolios(self):
        n = 10
        for i in range(n):
            o = models.Profile(
                user=User.objects.create_user("user #{}".format(i + 1)),
                first_name="a",
                last_name="b",
                contact_mail="a@a.com",
                short_description="I am",
            )
            o.full_clean()
            o.save()
        self.assertEquals(models.Profile.objects.all().count(), n)
