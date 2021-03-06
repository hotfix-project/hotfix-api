from .models import Category, System, App, Version, Patch
from rest_framework import viewsets, permissions, status as HTTPStatus
from .serializers import CategorySerializer, SystemSerializer, AppSerializer
from .serializers import VersionSerializer, PatchSerializer
from rest_framework import filters
from django.http import HttpResponse
from django.db import transaction
from django.db.models import F
import json


class DefaultsMixin(object):
    permission_classes = (
        permissions.IsAuthenticated,
    )


class CategoryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SystemViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer


class AppViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('category_id', 'system_id')
    ordering_fields = ('id', 'name', 'system_id', 'category_id')
    ordering = ('name', 'system_id', 'category_id')


class VersionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('app_id',)
    ordering_fields = ('id', 'name', 'create_time')
    ordering = ('-name', '-create_time')


class PatchViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Patch.objects.all()
    serializer_class = PatchSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('version_id',)
    ordering_fields = ('id', 'size', 'create_time', 'update_time', 'serial_number')


@transaction.atomic
def check_update(request):
    app_id = request.GET.get('app_id')
    if app_id is None or not isinstance(app_id, (str)) or not app_id.isdigit():
        status = HTTPStatus.HTTP_400_BAD_REQUEST
        data = {
            "status": status,
            "message": "query param app_id is required or incorrect type"
        }
        return HttpResponse(
            json.dumps(data, ensure_ascii=False), 
            content_type="application/json; charset=UTF-8",
            status=status
        )
    version = request.GET.get('version')
    if version is None or not isinstance(version, (str)):
        status = HTTPStatus.HTTP_400_BAD_REQUEST
        data = {
            "status": status,
            "message": "query param version is required or incorrect type"
        }
        return HttpResponse(
            json.dumps(data, ensure_ascii=False), 
            content_type="application/json; charset=UTF-8",
            status=status
        )
    apps = App.objects.filter(id=app_id)
    if apps.count() == 0:
        status = HTTPStatus.HTTP_404_NOT_FOUND
        data = {
            "status": status,
            "message": "app is not found"
        }
        return HttpResponse(
            json.dumps(data, ensure_ascii=False), 
            content_type="application/json; charset=UTF-8",
            status=status
        )
    versions = Version.objects.filter(app_id=app_id, name=version)
    if versions.count() == 0:
        status = HTTPStatus.HTTP_404_NOT_FOUND
        data = {
            "status": status,
            "message": "version is not found"
        }
        return HttpResponse(
            json.dumps(data, ensure_ascii=False), 
            content_type="application/json; charset=UTF-8",
            status=status
        )
    selected = (Patch.STATUS_RELEASED, Patch.STATUS_PRERELEASED, Patch.STATUS_DELETED)
    patchs = Patch.objects.select_for_update().filter(version_id=versions[0].id, status__in=selected)

    releases = patchs.filter(
        status__in=(Patch.STATUS_PRERELEASED, Patch.STATUS_RELEASED), download_count__lt=F('pool_size'))
    deletes = patchs.filter(status=Patch.STATUS_DELETED)

    status = HTTPStatus.HTTP_200_OK
    data = {
        "status": status,
        "message": "ok",
        "result": {
            "id": apps[0].id,
            "version": versions[0].name,
            "rsa": apps[0].rsa,
            "patch": {
                "released": list(releases.values('id', 'download_url', 'md5sum', 'pool_size')),
                "deleted": list(deletes.values('id')),
            }
        }
    }

    for patch in releases:
        patch.download_count = patch.download_count + 1
        patch.supersave()

    return HttpResponse(
        json.dumps(data, ensure_ascii=False), 
        content_type="application/json; charset=UTF-8",
        status=status
    )


@transaction.atomic
def report_update(request):
    patch_id = request.GET.get('patch_id')
    if patch_id is None or not isinstance(patch_id, (str)) or not patch_id.isdigit():
        status = HTTPStatus.HTTP_400_BAD_REQUEST
        data = {
            "status": status,
            "message": "query param patch_id is required or incorrect type"
        }
        return HttpResponse(
            json.dumps(data, ensure_ascii=False), 
            content_type="application/json; charset=UTF-8",
            status=status
        )
    patchs = Patch.objects.select_for_update().filter(id=patch_id)
    if len(patchs) == 0:
        status = HTTPStatus.HTTP_404_NOT_FOUND
        data = {
            "status": status,
            "message": "patch is not found"
        }
        return HttpResponse(
            json.dumps(data, ensure_ascii=False), 
            content_type="application/json; charset=UTF-8",
            status=status
        )

    # id is primary_key
    patchs[0].apply_count = patchs[0].apply_count + 1
    patchs[0].supersave()

    status = HTTPStatus.HTTP_200_OK
    data = {
       "status": status,
       "result": {
           "id": patch_id,
       },
       "message": "ok",
    }

    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json; charset=UTF-8")
