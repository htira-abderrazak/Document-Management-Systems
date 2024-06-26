import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DMS.settings')

app = Celery('DMS')
app.conf.enable_utc = False
#Execute every minute
app.conf.beat_schedule = {
    'periodic_delete': {
        'task': 'directory.tasks.periodic_delete',
        'schedule': crontab(minute='*/1', hour='*'),


    },
}
app.config_from_object('django.conf:settings' , namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')