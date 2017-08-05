# HotFix
HitFix patch manager

# Design
1. Restful API 
2. Web-apps
3. Using external storage services

# Ref
* [Quickstart](http://www.django-rest-framework.org/tutorial/quickstart/) 
* [Django Modle FieldType](https://docs.djangoproject.com/en/1.11/ref/models/fields/)

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

# TODO
1. Automatically distribute patch files, sync to release.remote\_url
