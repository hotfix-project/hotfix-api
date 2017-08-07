#!/bin/bash


 /usr/local/bin/gunicorn --worker-class=gevent project.wsgi:application -b 0.0.0.0:8000
# python3.6 manage.py runserver 0.0.0.0:8000
