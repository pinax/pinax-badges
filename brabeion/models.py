from datetime import datetime

from django.db import models

from django.contrib.auth.models import User



class BadgeAwarded(models.Model):
    user = models.ForeignKey(User, related_name="badges_earned")
    awarded_at = models.DateTimeField(default=datetime.now)
    slug = models.CharField(max_length=255)
    level = models.IntegerField()
    
    @property
    def badge(self):
        from brabeion.base import AwardedBadge
        return AwardedBadge(self.slug, self.level, self.user)
