from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class BadgeAwarded(models.Model):
    user = models.ForeignKey(User, related_name="badges_earned")
    awarded_at = models.DateTimeField(default=datetime.now)
    codename = models.CharField(max_length=255)
    level = models.IntegerField()
