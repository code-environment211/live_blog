# live_blog_project/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live_blog_project.settings')

app = Celery('live_blog_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
