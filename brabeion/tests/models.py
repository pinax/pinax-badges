from django.db import models


from brabeion.compat import AUTH_USER_MODEL


class PlayerStat(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, related_name="stats")
    points = models.IntegerField(default=0)
