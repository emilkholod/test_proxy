import pickle

from flask import Blueprint, Response, jsonify, make_response, request

from app import R_SERVER, celery

from . import celery_tasks, utils

bp = Blueprint('proxy', __name__)


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>', methods=utils.ALL_HTTP_METHODS)
def proxy(path):
    method = request.method
    hash = utils.get_hash_of_request(method, path)

    response_from_redis = None
    if R_SERVER.get(hash):
        R_SERVER.expire(hash, utils.EXPIRE_TIME_SEC)
        response_from_redis = pickle.loads(R_SERVER.get(hash))
    else:
        task = celery.AsyncResult(hash)
        if task.status == 'PENDING' or task.status == 'SUCCESS':
            task.forget()
            response = make_response(
                jsonify({
                    'PROXY INFO': 'Task was accepted for running',
                }), 200)
            task = celery_tasks.make_request_to_out.apply_async(
                args=(method, path),
                task_id=hash,
            )
        elif task.status == 'SENT':
            response = make_response(
                jsonify({
                    'PROXY INFO':
                    'Task has already been accepted for running. Wait for proccessing...',
                }), 200)
        else:
            task.forget()
            response = make_response(
                jsonify({
                    'PROXY WARNING': 'Task finished with another status',
                    'PROXY REQUEST DETAILS': {
                        'PROXY TASK STATUS': task.status,
                        'PROXY METHOD': method,
                        'PROXY PATH': path,
                    }
                }), 200)

    if response_from_redis is not None:
        response = Response(
            response_from_redis.content,
            response_from_redis.status_code,
        )
    return response
