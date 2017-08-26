from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "pinax.badges"
    label = "pinax_badges"
    verbose_name = _("Pinax Badges")
