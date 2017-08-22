#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "Operation not permitted"
    exit 1
fi

yum install -y mariadb-server mariadb-devel mariadb || exit 1

systemctl start mariadb
systemctl enable mariadb
mysql_secure_installation

firewall-cmd --permanent --add-service mysql
systemctl restart firewalld.service
