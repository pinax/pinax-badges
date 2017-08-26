from django.conf import settings
from django.db import models
from django.utils import timezone


class BadgeAward(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="badges_earned", on_delete=models.CASCADE)
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
        from .registry import badges
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
