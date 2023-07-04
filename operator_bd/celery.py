import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'account.settings.local')

app = Celery('operator_bd')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

