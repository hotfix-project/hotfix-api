# HotFix Rest API
[![Build Status](https://img.shields.io/travis/hotfix-project/hotfix-api.svg?branch=master)]( https://travis-ci.org/hotfix-project/hotfix-api) [![Requirements Status](https://requires.io/github/hotfix-project/hotfix-api/requirements.svg?branch=master)](https://requires.io/github/hotfix-project/hotfix-api/requirements/?branch=master) [![Coverage Status](https://coveralls.io/repos/github/hotfix-project/hotfix-api/badge.svg?branch=master)](https://coveralls.io/github/hotfix-project/hotfix-api?branch=master) [![Code Climate](https://codeclimate.com/github/hotfix-project/hotfix-api.png)](https://codeclimate.com/github/hotfix-project/hotfix-api)

# Design
1. Backend: REST API
2. Frontend: Web-apps
3. Using external storage services

# Requirements
* Python 3.6
* Django 
  * 1.10.7
  * 1.11.4
* [More](requirements.txt?raw=true)

# Install
1. download source
    ```
    git clone https://github.com/hotfix-project/hotfix-api.git
    ```
2. install python modules
    ```
    cd hotfix-api
    pip3.6 install -r requirements.txt
    ```
3. install mysql
    ```
    yum install mariadb-server mariadb-devel mariadb

    systemctl start mariadb
    systemctl enable mariadb
    mysql_secure_installation
    firewall-cmd --permanent --add-service mysql
    systemctl restart firewalld.service
    ```
4. init database
    ```
    sh init_db.sh
    ```
5. run
    ```  
    sh startup.sh
    ```

# Presentation

Click thumbnails to enlarge.

## Managing Categorys
[![Listing Categorys](screenshots/category_thumbnail.png)](screenshots/category.png?raw=true)

## Managing Systems
[![Listing Systems](screenshots/system_thumbnail.png)](screenshots/system.png?raw=true)

## Managing APPs
[![Listing Apps](screenshots/app_thumbnail.png)](screenshots/app.png?raw=true)

## Managing Versions
[![Listing Versions](screenshots/version_thumbnail.png)](screenshots/version.png?raw=true)

## Managing Patchs
[![Listing Patchs](screenshots/patch_thumbnail.png)](screenshots/patch.png?raw=true)


## Security
Only expose the api **check_update** to Internet

# Client workflow
1. Check update
2. Download patch&Decrypt patch&Verification patch&Apply patch
3. Report update status
