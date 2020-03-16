Proxy app using Flask+Celery(as worker)+Redis(as cache and broker).

Install:
1) Create your own virtualenv (for example, test_flask)
2) Install packages with requirements
3) Change in activate_env.bat to your virtualenv name
4) Run start_app.bat
5) For example, you can send from cmd:
curl -X GET "http://httpbin.org/get" -H  "accept: application/json"
6) If this request is not in cache, then you will see message about it. Else you will get result of the request (content of the request).