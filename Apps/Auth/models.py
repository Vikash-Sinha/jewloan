from django.db import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
    GENDER = (('male', 'Male'), ('female', 'Female'), ('other', 'Other'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, default=None, blank=True)

    def __str__(self):
        return self.user.username
