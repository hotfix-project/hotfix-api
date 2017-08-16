#!/bin/bash

PWD=$(cd "$(dirname "$0")"; pwd)

cd ${PWD}
coverage run manage.py test -k
coverage run manage.py test -k -r

echo ""
echo "Coverage Report"
coverage report
