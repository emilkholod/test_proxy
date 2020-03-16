import hashlib

import requests

FUNC_FOR_ALL_HTTP_METHODS = {
    'GET': lambda x: requests.get(x),
    'POST': lambda x: requests.post(x),
    'DELETE': lambda x: requests.delete(x),
    'PATCH': lambda x: requests.patch(x),
    'PUT': lambda x: requests.put(x),
}
ALL_HTTP_METHODS = list(FUNC_FOR_ALL_HTTP_METHODS.keys())
SITE_NAME = 'http://httpbin.org/'
EXPIRE_TIME_SEC = 600


def get_hash_of_request(method, path):
    method_hash = hashlib.sha1(method.encode()).hexdigest()
    path_hash = hashlib.sha1(path.encode()).hexdigest()
    hash = method_hash + path_hash
    return hash
