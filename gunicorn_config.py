import multiprocessing

bind = '127.0.0.1:8081'

workers = 2

accesslog = '/var/tmp/gunicorn_access.log'
errorlog = '/var/tmp/gunicorn_error.log'
