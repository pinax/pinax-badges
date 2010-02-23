from django.conf.urls.defaults import *



urlpatterns = patterns("",
    url(r"^$", "brabeion.views.list_badges", name="badges"),
    url(r"^(\w+)/(\d+)/$", "brabeion.views.badge_detail", name="badge_detail"),
)
