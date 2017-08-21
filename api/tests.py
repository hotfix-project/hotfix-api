from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, System, App, Version, Patch
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import json
import uuid
import sys

def set_credentials(client):
    user = User.objects.create_superuser('admin', 'admin@admin.com', '123456@admin')
    user.save()

    url = '/api-token-auth/'
    data = {'username': 'admin', 'password':'123456@admin'}
    response = client.post(url, data, format='json')
    token = json.loads(response.content)['token']
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)


def create_category(client):
    url = '/api/categorys'
    data = {'name': 'Finance'}
    return client.post(url, data, format='json')


def create_system(client):
    url = '/api/systems'
    data = {'name': 'Android'}
    return client.post(url, data, format='json')


def create_app(client, category_id, system_id, name):
    url = '/api/apps'
    data = {
        'name': name,
        'category_id': 'http://127.0.0.1/api/categorys/' + str(category_id),
        'system_id': 'http://127.0.0.1/api/systems/' + str(system_id), 
        'key': 'key',
        'secret': 'secret',
        'rsa': 'rsa'
    }
    return client.post(url, data, format='json')
 

def create_version(client, app_id, version_name):
    url = '/api/versions'
    data = {
        'app_id': 'http://127.0.0.1/api/apps/' + str(app_id),
        'name': version_name, 
    }
    return client.post(url, data, format='json')
 

def create_patch(client, version_id, status=Patch.STATUS_WAITING, pool_size=sys.maxsize):
    url = '/api/patchs'
    data = {
        'version_id': 'http://127.0.0.1/api/versions/' + str(version_id),
        'desc': 'a patch', 
        'download_url': 'http://www.baidu.com/', 
        'size': 1000, 
        'status': status,
        'pool_size': pool_size,
    }
    return client.post(url, data, format='json')
 

def list_category(client):
    url = '/api/categorys'
    return client.get(url)


def list_system(client):
    url = '/api/systems'
    return client.get(url)


def list_app(client):
    url = '/api/apps'
    return client.get(url)


def list_version(client):
    url = '/api/versions'
    return client.get(url)


def list_patch(client):
    url = '/api/patchs'
    return client.get(url)


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

    def test_auth401_create_category(self):
        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth401_list_category(self):
        response = list_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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

    def test_auth401_create_system(self):
        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth401_list_system(self):
        response = list_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(App.objects.count(), 1)
        self.assertEqual(App.objects.get(name=app_name).name, app_name)

    def test_auth401_create_app(self):
        app_name = uuid.uuid4().hex
        response = create_app(self.client, 0, 0, app_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth401_list_app(self):
        response = list_app(self.client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app_id = App.objects.get(name=app_name).id

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app_id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(App.objects.count(), 1)
        self.assertEqual(Version.objects.get(name=version_name).name, version_name)

    def test_auth401_create_version(self):
        version_name = uuid.uuid4().hex
        response = create_version(self.client, 0, version_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth401_list_version(self):
        response = list_version(self.client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app_id = App.objects.get(name=app_name).id

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app_id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version_id = Version.objects.get(name=version_name).id

        response = create_patch(self.client, version_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")

    def test_auth401_create_patch(self):
        response = create_patch(self.client, 0)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth401_list_patch(self):
        response = list_patch(self.client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CheckUpdateTests(APITestCase):
    def test_param_error_app_id(self):
        url = '/check_update'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"detail":"query param app_id is required"}')
    def test_param_error_version(self):
        url = '/check_update?app_id=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"detail":"query param version is required"}')
    def test_app_not_found(self):
        url = '/check_update?app_id=1&version=1.1.1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content, b'{"detail":"app is not found"}')
    def test_version_not_found(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app_id = App.objects.get(name=app_name).id

        url = '/check_update?app_id=%s&version=1.1.1' % (app_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content, b'{"detail":"version is not found"}')
    def test_patch_not_found(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        url = '/check_update?app_id=%s&version=%s' % (app.id, version.name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data["results"]["released"]), 0)
        self.assertEqual(len(data["results"]["deleted"]), 0)
    def test_patch_not_found_2(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")

        url = '/check_update?app_id=%s&version=%s' % (app.id, version.name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data["results"]["released"]), 0)
        self.assertEqual(len(data["results"]["deleted"]), 0)
    def test_patch_released(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id, status=Patch.STATUS_RELEASED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")

        url = '/check_update?app_id=%s&version=%s' % (app.id, version.name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data["results"]["released"]), 1)
        self.assertEqual(len(data["results"]["deleted"]), 0)
    def test_patch_prereleased(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        pool_size = 10
        response = create_patch(self.client, version.id, status=Patch.STATUS_PRERELEASED, pool_size=pool_size)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")

        for i in range(pool_size):
            url = '/check_update?app_id=%s&version=%s' % (app.id, version.name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            self.assertEqual(len(data["results"]["released"]), 1)
            self.assertEqual(len(data["results"]["deleted"]), 0)

        url = '/check_update?app_id=%s&version=%s' % (app.id, version.name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data["results"]["released"]), 0)
        self.assertEqual(len(data["results"]["deleted"]), 0)
    def test_patch_released_prereleased(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id, status=Patch.STATUS_RELEASED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)

        response = create_patch(self.client, version.id, status=Patch.STATUS_PRERELEASED, pool_size=100)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 2)

        url = '/check_update?app_id=%s&version=%s' % (app.id, version.name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data["results"]["released"]), 1)
        self.assertEqual(len(data["results"]["deleted"]), 0)
    def test_patch_prereleased_released(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id, status=Patch.STATUS_PRERELEASED, pool_size=100)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)

        response = create_patch(self.client, version.id, status=Patch.STATUS_RELEASED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 2)

        url = '/check_update?app_id=%s&version=%s' % (app.id, version.name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data["results"]["released"]), 1)
        self.assertEqual(len(data["results"]["deleted"]), 0)
 
    def test_patch_deleted(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id, status=Patch.STATUS_RELEASED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)

        response = create_patch(self.client, version.id, status=Patch.STATUS_PRERELEASED, pool_size=100)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 2)

        response = create_patch(self.client, version.id, status=Patch.STATUS_DELETED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 3)

        url = '/check_update?app_id=%s&version=%s' % (app.id, version.name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data["results"]["released"]), 1)
        self.assertEqual(len(data["results"]["deleted"]), 1)
    def test_patch_pool_size_and_download_count(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        pool_size = 10
        response = create_patch(self.client, version.id, status=Patch.STATUS_PRERELEASED, pool_size=pool_size)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")

        for i in range(pool_size*2):
            url = '/check_update?app_id=%s&version=%s' % (app.id, version.name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        patch = Patch.objects.get(version_id=version.id, status=Patch.STATUS_PRERELEASED) 
        self.assertEqual(patch.pool_size, 0)
        self.assertEqual(patch.download_count, pool_size)
    def test_patch_download_count(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        pool_size = 10
        response = create_patch(self.client, version.id, status=Patch.STATUS_RELEASED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)

        for i in range(pool_size*2):
            url = '/check_update?app_id=%s&version=%s' % (app.id, version.name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        patch = Patch.objects.get(version_id=version.id, status=Patch.STATUS_RELEASED) 
        self.assertEqual(patch.download_count, pool_size*2)


class CheckReportTests(APITestCase):
    def test_param_error_patch_id(self):
        url = '/report_update'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"detail":"query param patch_id is required"}')
    def test_patch_not_found(self):
        url = '/report_update?patch_id=0'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content, b'{"detail":"patch is not found"}')
    def test_patch_wating(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id)
        patch = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")

        apply_count = 10
        url = '/report_update?patch_id=%s' % (patch["id"])
        for i in range(apply_count):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        patch = Patch.objects.get(id=patch["id"]) 
        self.assertEqual(patch.apply_count, apply_count)
    def test_patch_stoped(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id, status=Patch.STATUS_STOPED)
        patch = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")

        apply_count = 10
        url = '/report_update?patch_id=%s' % (patch["id"])
        for i in range(apply_count):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        patch = Patch.objects.get(id=patch["id"]) 
        self.assertEqual(patch.apply_count, apply_count)
    def test_patch_released(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id, status=Patch.STATUS_RELEASED)
        patch = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")

        apply_count = 10
        url = '/report_update?patch_id=%s' % (patch["id"])
        for i in range(apply_count):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        patch = Patch.objects.get(id=patch["id"]) 
        self.assertEqual(patch.apply_count, apply_count)
    def test_patch_prereleased(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id, status=Patch.STATUS_PRERELEASED)
        patch = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")

        apply_count = 10
        url = '/report_update?patch_id=%s' % (patch["id"])
        for i in range(apply_count):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        patch = Patch.objects.get(id=patch["id"]) 
        self.assertEqual(patch.apply_count, apply_count)
    def test_patch_deleted(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id, status=Patch.STATUS_DELETED)
        patch = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Patch.objects.get(desc='a patch').desc, "a patch")

        apply_count = 10
        url = '/report_update?patch_id=%s' % (patch["id"])
        for i in range(apply_count):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        patch = Patch.objects.get(id=patch["id"]) 
        self.assertEqual(patch.apply_count, apply_count)
    def test_patch_pool_size_default(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id, status=Patch.STATUS_WAITING)
        patch = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(patch["pool_size"], sys.maxsize)
    def test_patch_serial_number(self):
        set_credentials(self.client)

        response = create_category(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.get(name='Finance').id

        response = create_system(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        system_id = System.objects.get(name='Android').id

        app_name = uuid.uuid4().hex
        response = create_app(self.client, category_id, system_id, app_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app = App.objects.get(name=app_name)

        version_name = uuid.uuid4().hex
        response = create_version(self.client, app.id, version_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        version = Version.objects.get(name=version_name)

        response = create_patch(self.client, version.id, status=Patch.STATUS_WAITING)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        patch = json.loads(response.content)
        serial_number = patch["serial_number"]
        self.assertEqual(serial_number, 1)

        response = create_patch(self.client, version.id, status=Patch.STATUS_RELEASED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        patch = json.loads(response.content)
        serial_number = patch["serial_number"]
        self.assertEqual(serial_number, 2)

        response = create_patch(self.client, version.id, status=Patch.STATUS_PRERELEASED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        patch = json.loads(response.content)
        serial_number = patch["serial_number"]
        self.assertEqual(serial_number, 3)

        response = create_patch(self.client, version.id, status=Patch.STATUS_WAITING)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        patch = json.loads(response.content)
        serial_number = patch["serial_number"]
        self.assertEqual(serial_number, 4)

