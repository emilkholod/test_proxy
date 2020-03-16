import os

from celery import Celery


def make_celery(app):
    if os.name == 'nt':
        os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['app.celery_tasks'],
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
