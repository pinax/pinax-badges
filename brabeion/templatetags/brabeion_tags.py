from django import template

from brabeion.models import BadgeAward


register = template.Library()


class BadgeCountNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 2:
            return cls(bits[1])
        elif len(bits) == 4:
            if bits[2] != "as":
                raise template.TemplateSyntaxError("Second argument to %r must "
                    "be 'as'" % bits[0])
            return cls(bits[1], bits[3])
        raise template.TemplateSyntaxError("%r takes either 1 or 3 arguments." % bits[0])
    
    def __init__(self, user, context_var=None):
        self.user = template.Variable(user)
        self.context_var = context_var
    
    def render(self, context):
        user = self.user.resolve(context)
        badge_count = BadgeAward.objects.filter(user=user).count()
        if self.context_var is not None:
            context[self.context_var] = badge_count
            return ""
        return unicode(badge_count)

@register.tag
def badge_count(parser, token):
    """
    Returns badge count for a user, valid usage is::

        {% badge_count user %}
    
    or
    
        {% badge_count user as badges %}
    """
    return BadgeCountNode.handle_token(parser, token)


class BadgesForUserNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) != 4:
            raise template.TemplateSyntaxError("%r takes exactly 3 arguments." % bits[0])
        if bits[2] != "as":
            raise template.TemplateSyntaxError("The 2nd argument to %r should "
                "be 'as'" % bits[0])
        return cls(bits[1], bits[3])
    
    def __init__(self, user, context_var):
        self.user = template.Variable(user)
        self.context_var = context_var
    
    def render(self, context):
        user = self.user.resolve(context)
        context[self.context_var] = BadgeAward.objects.filter(
            user=user
        ).order_by("-awarded_at")
        return ""
        

@register.tag
def badges_for_user(parser, token):
    """
    Sets the badges for a given user to a context var.  Usage:
        
        {% badges_for_user user as badges %}
    """
    return BadgesForUserNode.handle_token(parser, token)
