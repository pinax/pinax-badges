from brabeion.models import BadgeAward
from brabeion.signals import badge_awarded



class BadgeAwarded(object):
    def __init__(self, level=None, user=None):
        self.level = level
        self.user = user


class BadgeDetail(object):
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description


class Badge(object):
    async = False

    def __init__(self):
        assert not (self.multiple and len(self.levels) > 1)
        for i, level in enumerate(self.levels):
            if not isinstance(level, BadgeDetail):
                self.levels[i] = BadgeDetail(level)

    def possibly_award(self, **state):
        """
        Will see if the user should be awarded a badge.  If this badge is
        asynchronous it just queues up the badge awarding.
        """
        assert "user" in state
        if self.async:
            from brabeion.tasks import AsyncBadgeAward
            state = self.freeze(**state)
            AsyncBadgeAward.delay(self, state)
            return
        self.actually_possibly_award(**state)

    def actually_possibly_award(self, **state):
        """
        Does the actual work of possibly awarding a badge.
        """
        user = state["user"]
        force_timestamp = state.pop("force_timestamp", None)
        awarded = self.award(**state)
        if awarded is None:
            return
        if awarded.level is None:
            assert len(self.levels) == 1
            awarded.level = 1
        # awarded levels are 1 indexed, for conveineince
        awarded = awarded.level - 1
        assert awarded < len(self.levels)
        if (not self.multiple and
            BadgeAward.objects.filter(user=user, slug=self.slug, level=awarded)):
            return
        extra_kwargs = {}
        if force_timestamp is not None:
            extra_kwargs["awarded_at"] = force_timestamp
        badge = BadgeAward.objects.create(user=user, slug=self.slug,
            level=awarded, **extra_kwargs)
        badge_awarded.send(sender=self, badge_award=badge)

    def freeze(self, **state):
        return state


def send_badge_messages(badge_award, **kwargs):
    """
    If the Badge class defines a message, send it to the user who was just
    awarded the badge.
    """
    user_message = getattr(badge_award.badge, "user_message", None)
    if callable(user_message):
        message = user_message(badge_award)
    else:
        message = user_message
    if message is not None:
        badge_award.user.message_set.create(message=message)
badge_awarded.connect(send_badge_messages)
