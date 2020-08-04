from __future__ import absolute_import
import os
import django
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


# app.autodiscover_tasks()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsapi.settings')
django.setup()

app = Celery('newsapi')


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
 

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


CELERYBEAT_SCHEDULE = {
    'add-every-monday-morning': {
       'task': 'tasks.reset_number_request',
       'schedule': crontab(hour=3, minute=10),
       'args': (16, 16),
   },
}
