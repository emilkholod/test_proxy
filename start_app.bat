start CMD /K "activate_env.bat & celery flower --broker=redis://"
start CMD /K "activate_env.bat & celery worker -A app.celery --loglevel=info"
start CMD /K "activate_env.bat & flask run"
