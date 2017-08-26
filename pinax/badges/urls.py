from django.conf.urls import url

from .views import badge_list, badge_detail


urlpatterns = [
    url(r"^$", badge_list, name="badge_list"),
    url(r"^(\w+)/(\d+)/$", badge_detail, name="badge_detail"),
]
