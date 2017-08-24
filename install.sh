#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "Operation not permitted"
    exit 1
fi

curl https://raw.githubusercontent.com/WALL-E/static/master/setup/redhat/install_python36|bash

pip3.6 install -r requirements.txt
