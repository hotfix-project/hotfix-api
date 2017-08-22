#!/bin/bash

PWD=$(cd "$(dirname "$0")"; pwd)

command -v "mysql" > /dev/null
ret=$?

if test $ret -ne 0
then
    echo "You need to install MySQL database"
    exit 1
else
    mysql < ${PWD}/create_database.sql
fi
