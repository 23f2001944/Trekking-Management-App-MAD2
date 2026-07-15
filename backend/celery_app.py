from celery import Celery
from celery.schedules import crontab

celery = Celery(
    'tma',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
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