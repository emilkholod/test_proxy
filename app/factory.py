from flask import Flask

from app import celery

from . import celery_util


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.update(CELERY_BROKER_URL='redis://',
                        CELERY_RESULT_BACKEND='redis://')

    celery_util.init_celery(flask_app, celery)

    with flask_app.app_context():
        from .routes import bp as proxy_bp
        flask_app.register_blueprint(proxy_bp)
    return flask_app
