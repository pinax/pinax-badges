from django import template

from pinax.badges.models import BadgeAward

register = template.Library()


@register.simple_tag
def badge_count(user):
    """
    Returns badge count for a user, valid usage is::

        {% badge_count user %}

    or

        {% badge_count user as badges %}
    """
    return BadgeAward.objects.filter(user=user).count()


@register.simple_tag
def badges_for_user(user):
    """
    Sets the badges for a given user to a context var.  Usage:

        {% badges_for_user user as badges %}
    """
    return BadgeAward.objects.filter(user=user).order_by("-awarded_at")
