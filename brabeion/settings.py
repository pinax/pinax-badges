from django.conf import settings
from django.utils import importlib

USER_SETTINGS = getattr(settings, 'BRABEION', None)

DEFAULTS = {
    'ABSTRACT_MODEL': False,
    'BADGEAWARD_MODEL': 'brabeion.models.BadgeAward'
}

IMPORT_STRINGS = (
    'BADGEAWARD_MODEL'
)


class Settings(object):
    """
    For example:
        >>> from brabeion.settings import brabeion_settings
        >>> print brabeion_settings.BADGEAWARD_MODEL
    """
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    def import_from_string(self, val, setting_name):
        """
        Attempt to import a class from a string representation.
        """
        try:
            parts = val.split('.')
            module_path, class_name = '.'.join(parts[:-1]), parts[-1]
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        except ImportError as e:
            msg = "Could not import '%s' for setting '%s'. %s: %s." % (
                val, setting_name, e.__class__.__name__, e)
            raise ImportError(msg)

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid setting: '%s'" % attr)

        val = self.defaults[attr]
        if attr in self.user_settings.keys():
            val = self.user_settings[attr]

        if attr in self.import_strings:
            return self.import_from_string(val, attr)

        return val

brabeion_settings = Settings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
