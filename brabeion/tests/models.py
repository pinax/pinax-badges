from django.db import models

try:
    from django.contrib.auth import get_user_model
except ImportError:
    # Prior to Django 1.5, the AUTH_USER_MODEL setting does not exist.
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class PlayerStat(models.Model):
    user = models.OneToOneField(User, related_name="stats")
    points = models.IntegerField(default=0)
