try:
    from celery import Task
    from celery.registry import tasks
except ImportError:
    # If celery is not installed, just use a stub base class
    Task = object


class AsyncBadgeAward(Task):
    ignore_result = True

    def run(self, badge, state, **kwargs):
        badge.actually_possibly_award(**state)


tasks.register(AsyncBadgeAward)
