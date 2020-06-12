from collections import defaultdict

from django.db.models import Count
from django.shortcuts import render

from .models import BadgeAward
from .registry import badges


def badge_list(request):
    if request.user.is_authenticated:
        user_badges = {
            (slug, level) for slug, level in
            BadgeAward.objects.filter(user=request.user).values_list("slug", "level")
        }
    else:
        user_badges = []
    badges_awarded = BadgeAward.objects.values("slug", "level").annotate(num=Count("pk"))
    badges_dict = defaultdict(list)
    for badge in badges_awarded:
        badges_dict[badge["slug"]].append({
            "level": badge["level"],
            "name": badges._registry[badge["slug"]].levels[badge["level"]].name,
            "description": badges._registry[badge["slug"]].levels[badge["level"]].description,
            "count": badge["num"],
            "user_has": (badge["slug"], badge["level"]) in user_badges
        })

    for badge_group in badges_dict.values():
        badge_group.sort(key=lambda o: o["level"])

    return render(request, "pinax/badges/badges.html", {
        "badges": sorted(badges_dict.items()),
    })


def badge_detail(request, slug, level):
    badge = badges._registry[slug].levels[int(level)]
    badge_awards = BadgeAward.objects.filter(
        slug=slug,
        level=level
    ).order_by("-awarded_at")

    badge_count = badge_awards.count()
    latest_awards = badge_awards[:50]

    return render(request, "pinax/badges/badge_detail.html", {
        "badge": badge,
        "badge_count": badge_count,
        "latest_awards": latest_awards,
    })
