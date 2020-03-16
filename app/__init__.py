import redis
from celery import Celery

R_SERVER = redis.StrictRedis()

celery = Celery(
    'app.factory',
    include=['app.celery_tasks'],
)
