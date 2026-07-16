from dotenv import load_dotenv
import os
from celery import Celery
from celery.schedules import crontab

load_dotenv()

celery = Celery(
    'tma',
    broker=f"redis://{os.getenv('REDIS_HOST','localhost')}:{os.getenv('REDIS_PORT',6379)}/{os.getenv('CELERY_BROKER_DB',0)}",
    backend=f"redis://{os.getenv('REDIS_HOST','localhost')}:{os.getenv('REDIS_PORT',6379)}/{os.getenv('CELERY_BACKEND_DB',1)}",
    include=['tasks'],
)

celery.conf.beat_schedule = {
    'daily-trek-reminders': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=8, minute=0),   # every day at 8:00 AM
    },
    'monthly-admin-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(hour=6, minute=0, day_of_month=1),  # 1st of each month, 6 AM
    },
}
celery.conf.timezone = 'Asia/Kolkata'