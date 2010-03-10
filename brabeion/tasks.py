from celery.task import Task



class AsyncBadgeAward(Task):
    ignore_result = True
    
    def run(self, badge, state, **kwargs):
        badge.actually_possibly_award(**state)
