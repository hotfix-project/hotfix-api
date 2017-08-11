#!/bin/bash

PWD=$(cd "$(dirname "$0")"; pwd)

cd ${PWD}

python3.6 manage.py makemigrations
python3.6 manage.py migrate
