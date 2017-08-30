#!/bin/bash

PWD=$(cd "$(dirname "$0")"; pwd)

cd ${PWD}
coverage run manage.py test -k --failfast
coverage run manage.py test -k -r --failfast

echo ""
echo "Coverage Report"
coverage report
