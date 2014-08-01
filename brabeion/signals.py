from django.dispatch import Signal


badge_awarded = Signal(providing_args=["badge"])
