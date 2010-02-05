from celery.task import Task


class AsyncBadgeAward(Task):
    def run(self, badge, state, **kwargs):
        badge.actually_possibly_award(**state)
