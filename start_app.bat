start CMD /K "activate_env.bat & celery flower --broker=redis://"
start CMD /K "activate_env.bat & celery worker -A indirect_start_app.celery --loglevel=info"
start CMD /K "activate_env.bat & python indirect_start_app.py"
