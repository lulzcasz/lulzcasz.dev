from celery import Celery

app = Celery('lulzcasz')

app.autodiscover_tasks()

app.config_from_object('django.conf:settings', namespace='CELERY')
