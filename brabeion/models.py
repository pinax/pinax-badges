from django.db import models
from django.utils import timezone

try:
    from django.contrib.auth import get_user_model
except ImportError:
    # Prior to Django 1.5, the AUTH_USER_MODEL setting does not exist.
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class BadgeAward(models.Model):
    user = models.ForeignKey(User, related_name="badges_earned")
    awarded_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=255)
    level = models.IntegerField()

    def __getattr__(self, attr):
        return getattr(self._badge, attr)

    @property
    def badge(self):
        return self

    @property
    def _badge(self):
        from brabeion import badges
        return badges._registry[self.slug]

    @property
    def name(self):
        return self._badge.levels[self.level].name

    @property
    def description(self):
        return self._badge.levels[self.level].description

    @property
    def progress(self):
        return self._badge.progress(self.user, self.level)
