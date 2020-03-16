from app import celery
from app.celery_util import init_celery
from app.factory import create_app

app = create_app()
init_celery(app, celery)

if __name__ == '__main__':
    app.run()
