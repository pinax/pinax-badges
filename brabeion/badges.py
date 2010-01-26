from collections import defaultdict

from brabeion.models import BadgeAward


class BadgeCache(object):
    """
    This is responsible for storing all badges that have been registered, as
    well as providing the pulic API for awarding badges.
    
    This class should not be instantiated multiple times, if you do it's your
    fault when things break, and you get to pick up all the pieces.
    """
    def __init__(self):
        self._event_registry = defaultdict(list)
        self._registry = {}
    
    def register(self, badge):
        # We should probably duck-type this, but for now it's a decent sanity
        # check.
        assert issubclass(badge, Badge)
        badge = Badge()
        self._registry[badge.name] = badge
        for event in badge.events:
            self._event_registry[event].append(badge)
    
    def possibly_award_badge(self, event, **state):
        for badge in self._registry[event]:
            badge.possibly_award(**state)


class BadgeAwarded(object):
    def __init__(self, level=None):
        self.level = level

class BadgeDetail(object):
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description


class Badge(object):
    def __init__(self):
        assert not (self.multiple and len(self.levels) > 1)
        for i, level in enumerate(self.levels):
            if not isinstance(level, BadgeDetail):
                self.levels[i] = BadgeDetail(level)
    
    def possibly_award(self, **state):
        assert "user" in state
        if (not self.multiple and
            BadgeAward.objects.filter(user=state["user"]).exists()):
            # if the user has this badge, and they can't get it more than once
            # bail early
            return
        if self.async:
            raise NotImplementedError("I haven't implemented async Badge's yet")

        awarded = self.award(**state)
        if awarded is None:
            return
        if awarded.level is None:
            assert len(self.levels) == 1
            awarded.level = 1
        # awarded levels are 1 indexed, for conveineince
        awarded = awarded.level - 1
        assert awarded < len(self.levels)
        BadgeAward.objects.create(user=state["user"], codename=self.name,
            level=awarded)


class AwardedBadge(object):
    def __init__(self, codename, level, user):
        self.codename = codename
        self.level = level
        self.user = user
        self._badge = badges._registry[codename]
    
    @property
    def name(self):
        return self._badge.levels[self.level].name
    
    @property
    def description(self):
        return self._badge.levels[self.level].description
    
    @property
    def progress(self):
        return self._badge.progress(self.user, self.level)


badges = BadgeCache()
