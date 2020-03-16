import os


def init_celery(app, celery):
    if os.name == 'nt':
        os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

    celery.conf['result_backend'] = app.config['CELERY_BROKER_URL']
    celery.conf['broker_url'] = app.config['CELERY_RESULT_BACKEND']

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
