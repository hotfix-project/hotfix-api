#!/bin/bash

PYTHON=python3.6
PWD=`cd "$(dirname "$0")"; pwd`
PATCH=$PWD/documentation.patch
MODULE=`python3.6 -c "import os;import rest_framework;print(rest_framework.__file__)"`

cd `dirname ${MODULE}`
patch -p1 < $PATCH
cd -
