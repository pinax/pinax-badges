from django.conf import settings
from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase

from pinax.badges.base import Badge, BadgeAwarded
from pinax.badges.registry import badges
from pinax.badges.templatetags import pinax_badges_tags

from .models import PlayerStat


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

    def test_async_attribute(self):
        b = PointsBadge()
        self.assertEqual(b.async_, False)
        self.assertEqual(getattr(b, "async"), False)

        setattr(b, "async", True)
        self.assertEqual(b.async_, True)
        self.assertEqual(getattr(b, "async"), True)

    def test_undefined_attribute_error_message(self):
        with self.assertRaises(NotImplementedError):
            Badge()


class TemplateTagsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("Lars Bak", "lars@hotspot.com", "x864lyfe")
        PlayerStat.objects.create(user=self.user)
        self.user.stats.points += 5001
        self.user.stats.save()
        badges.possibly_award_badge("points_awarded", user=self.user)

    def test_badge_count(self):
        self.assertEqual(pinax_badges_tags.badge_count(self.user), 1)

    def test_badges_for_user(self):
        self.assertEqual(pinax_badges_tags.badges_for_user(self.user).count(), 1)


class TasksTestCase(TestCase):

    def test_import_without_celery(self):
        # importing pinax.badges.tasks without celery installed should not fail
        try:
            import pinax.badges.tasks  # noqa
        except ImportError:
            self.fail("Importing pinax.badges.tasks without celery installed should not fail")
