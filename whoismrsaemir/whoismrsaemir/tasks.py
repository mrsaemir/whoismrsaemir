from celery.schedules import crontab
from celery.task import periodic_task
from django.http import HttpRequest
from .views import check_queue


@periodic_task(run_every=crontab(minute=0, hour=0))
def check_queue_job():
    request = HttpRequest()
    check_queue(request=request)
