from django.conf import settings


__all__ = ['get_user_model', 'AUTH_USER_MODEL']


def get_user_model():
    """ Returns the appropriate User model class. As of Django 1.5, the use
    of custom user models was allowed by changing a setting. This method
    will no longer be required when Django 1.4 support is dropped.
    """
    try:
        # Django 1.5+
        from django.contrib.auth import get_user_model
        model = get_user_model()
    except ImportError:
        # Django <= 1.4
        from django.contrib.auth.models import User
        model = User
    return model

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
