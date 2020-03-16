import pickle

import app
from app import R_SERVER, celery, utils
from celery.signals import after_task_publish


@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    task = celery.tasks.get(sender)
    backend = task.backend if task else celery.backend
    backend.store_result(headers['id'], None, "SENT")


@app.celery.task(time_limit=60)
def make_request_to_out(method, path):
    hash = utils.get_hash_of_request(method, path)
    resp = utils.FUNC_FOR_ALL_HTTP_METHODS[method](utils.SITE_NAME + path)
    R_SERVER.set(hash, pickle.dumps(resp), ex=utils.EXPIRE_TIME_SEC)
