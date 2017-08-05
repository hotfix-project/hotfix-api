# HotFix
HitFix patch manager

# Tutorial
We're going to create a simple API to allow admin users to view and edit the users and groups in the system.

[Quickstart](http://www.django-rest-framework.org/tutorial/quickstart/) 

# Requirements
* Python 3.6+
* Django 1.11.4+
* MySQLdb
* djangorestframework
* markdown
* django-filter

# A-line-Shell
cmdline help
```
# init project
django-admin.py startproject project
django-admin.py startapp app
cd ..

# init database 
python3.6 manage.py migrate
python3.6 manage.py createsuperuser


# reinit database
python3.6 manage.py makemigrations
python3.6 manage.py migrate
python3.6 manage.py showmigrations

# run
python3.6 manage.py runserver 0.0.0.0:8000
```
