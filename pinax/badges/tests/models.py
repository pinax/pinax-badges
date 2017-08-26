from django.db import models

from django.contrib.auth.models import User


class PlayerStat(models.Model):
    user = models.OneToOneField(User, related_name="stats", on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
