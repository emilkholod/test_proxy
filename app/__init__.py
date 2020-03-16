from flask import Flask

import redis

from . import make_celery

R_SERVER = redis.StrictRedis()

flask_app = Flask('__main__')
flask_app.config.update(CELERY_BROKER_URL='redis://',
                        CELERY_RESULT_BACKEND='redis://')

celery = make_celery.make_celery(flask_app)
from app import routes
