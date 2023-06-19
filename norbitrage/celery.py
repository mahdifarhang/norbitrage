import os
from celery import Celery
# from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "norbitrage.settings")

app = Celery("norbitrage")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every_five_seconds-check_one_coin': {
        'task': 'check_coin_task',
        # 'schedule': crontab(minute='*/10', hour='2', day_of_week='8', day_of_month='*', month_of_year='*'),
        'schedule': 5,
        # 'args': (16, 16),
    },
    'every_ten_seconds-update_usdtirt_price': {
        'task': 'update_USDTIRT_cache_price',
        'schedule': 10,
    },
}