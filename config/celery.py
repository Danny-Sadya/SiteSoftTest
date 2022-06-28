import os
from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'main_page_scraper': {
        'task': 'src.posts.tasks.scrape_main_page',
        'schedule': crontab(minute='*/10')
    },
    'specific_posts_scraper': {
        'task': 'src.posts.tasks.scrape_specific_posts',
        'schedule': crontab(minute='*/1')
    }
}