from django.conf import settings
from django.db import connection
from django.test import TestCase

from brabeion import badges
from brabeion.base import Badge, BadgeAwarded
from brabeion.tests.models import PlayerStat

from brabeion.compat import get_user_model

User = get_user_model()


class PointsBadge(Badge):
    slug = "points"
    levels = [
        "Bronze",
        "Silver",
        "Gold",
    ]
    events = [
        "points_awarded",
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        points = user.stats.points
        if points > 10000:
            return BadgeAwarded(3)
        elif points > 7500:
            return BadgeAwarded(2)
        elif points > 5000:
            return BadgeAwarded(1)


badges.register(PointsBadge)


class BaseTestCase(TestCase):
    def assert_num_queries(self, n, func):
        current_debug = settings.DEBUG
        settings.DEBUG = True
        current = len(connection.queries)
        func()
        self.assertEqual(current + n, len(connection.queries), connection.queries[current:])
        settings.DEBUG = current_debug


class BadgesTests(BaseTestCase):
    def test_award(self):
        u = User.objects.create_user("Lars Bak", "lars@hotspot.com", "x864lyfe")
        PlayerStat.objects.create(user=u)
        badges.possibly_award_badge("points_awarded", user=u)
        self.assertEqual(u.badges_earned.count(), 0)

        u.stats.points += 5001
        u.stats.save()
        badges.possibly_award_badge("points_awarded", user=u)
        self.assertEqual(u.badges_earned.count(), 1)
        self.assertEqual(u.badges_earned.all()[0].badge.name, "Bronze")

        badges.possibly_award_badge("points_awarded", user=u)
        self.assertEqual(u.badges_earned.count(), 1)

        u.stats.points += 2500
        badges.possibly_award_badge("points_awarded", user=u)
        self.assertEqual(u.badges_earned.count(), 2)

    def test_lazy_user(self):
        u = User.objects.create_user("Lars Bak", "lars@hotspot.com", "x864lyfe")
        PlayerStat.objects.create(user=u, points=5001)
        badges.possibly_award_badge("points_awarded", user=u)
        self.assertEqual(u.badges_earned.count(), 1)

        self.assert_num_queries(1, lambda: u.badges_earned.get().badge)
