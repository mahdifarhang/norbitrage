import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "norbitrage.settings")

app = Celery("norbitrage")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'every_ten_seconds-check_coins': {
        'task': 'check_all_coins',
        # 'schedule': crontab(minute='*/10', hour='2', day_of_week='8', day_of_month='*', month_of_year='*'),
        'schedule': 10,
        # 'args': (16, 16),
    },
}