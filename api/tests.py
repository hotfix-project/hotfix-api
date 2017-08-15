from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, System, App, Version, Patch
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import json

def set_credentials(client):
    user = User.objects.create_superuser('admin', 'admin@admin.com', '123456@admin')
    user.save()

    url = '/api-token-auth/'
    data = {'username': 'admin', 'password':'123456@admin'}
    response = client.post(url, data, format='json')
    token = json.loads(response.content)['token']
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)


def create_category(client):
    url = '/hotfix/categorys'
    data = {'name': 'Finance'}
    return client.post(url, data, format='json')


def create_system(client):
    url = '/hotfix/systems'
    data = {'name': 'Android'}
    return client.post(url, data, format='json')


def create_app(client, category_id, system_id):
    url = '/hotfix/apps'
    data = {
        'name': 'iPos',
        'category_id': 'http://127.0.0.1/hotfix/categorys/' + str(category_id),
        'system_id': 'http://127.0.0.1/hotfix/systems/' + str(system_id), 
        'key': 'key',
        'secret': 'secret',
        'rsa': 'rsa'
    }
    return client.post(url, data, format='json')
 

def create_version(client, app_id):
    url = '/hotfix/versions'
    data = {
        'app_id': 'http://127.0.0.1/hotfix/apps/' + str(app_id),
        'name': '1.1.1', 
    }
    return client.post(url, data, format='json')
 

def create_patch(client, version_id):
    url = '/hotfix/patchs'
    data = {
        'version_id': 'http://127.0.0.1/hotfix/versions/' + str(version_id),
        'desc': 'a patch', 
        'download_url': 'http://www.baidu.com/', 
        'size': 1000, 
    }
    return client.post(url, data, format='json')
 

class CategoryTests(APITestCase):
    def test_create_category(self):
        """
        Ensure we can create a new Category object.
        """
        set_credentials(self.client)
        
        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get(name='Finance').name, "Finance")


class SystemTests(APITestCase):
    def test_create_system(self):
        """
        Ensure we can create a new System object.
        """
        set_credentials(self.client)

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(System.objects.count(), 1)
        self.assertEqual(System.objects.get(name='Android').name, "Android")


class AppTests(APITestCase):
    def test_create_app(self):
        """
        Ensure we can create a new App object.
        """
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        response = create_app(self.client, category_id, system_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(App.objects.count(), 1)
        self.assertEqual(App.objects.get(id=1).name, "iPos")


class VersionTests(APITestCase):
    def test_create_app(self):
        """
        Ensure we can create a new App object.
        """
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        response = create_app(self.client, category_id, system_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app_id = App.objects.get(name='iPos').id

        response = create_version(self.client, app_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(App.objects.count(), 1)
        self.assertEqual(Version.objects.get(name='1.1.1').name, "1.1.1")


class PatchTests(APITestCase):
    def test_create_app(self):
        """
        Ensure we can create a new App object.
        """
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        response = create_app(self.client, category_id, system_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app_id = App.objects.get(name='iPos').id

        response = create_version(self.client, app_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version_id = Version.objects.get(name='1.1.1').id

        response = create_patch(self.client, version_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")
