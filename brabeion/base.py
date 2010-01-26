from brabeion.models import BadgeAward


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
        if self.async:
            raise NotImplementedError("I haven't implemented async Badges yet")
        
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
            BadgeAward.objects.filter(user=state["user"], slug=self.slug, level=awarded)):
            return
        BadgeAward.objects.create(user=state["user"], slug=self.slug,
            level=awarded)
