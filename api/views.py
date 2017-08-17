from .models import Category, System, App, Version, Patch
from rest_framework import viewsets, permissions
from .serializers import CategorySerializer, SystemSerializer, AppSerializer
from .serializers import VersionSerializer, PatchSerializer
from rest_framework import filters
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
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
    ordering_fields = ('id', 'name')


class VersionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('app_id',)
    ordering_fields = ('id', 'name', 'create_time')


class PatchViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Patch.objects.all()
    serializer_class = PatchSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('version_id',)
    ordering_fields = ('id', 'size', 'create_time', 'update_time', 'serial_number')


def check_update(request):
    app_id = request.GET.get('app_id')
    if app_id is None:
        return HttpResponseBadRequest('{"detail":"query param app_id is required"}')
    version = page_num = request.GET.get('version')
    if version is None:
        return HttpResponseBadRequest('{"detail":"query param version is required"}')
    try:
        app = App.objects.get(id=app_id)
    except App.DoesNotExist:
        return HttpResponseNotFound('{"detail":"app is not found"}')
    try:
        version = Version.objects.get(app_id=app_id, name=version)
    except Version.DoesNotExist:
        return HttpResponseNotFound('{"detail":"version is not found"}')
    try:
        patch = Patch.objects.get(id=version.id, is_enable=True)
    except Patch.DoesNotExist:
        return HttpResponseNotFound('{"detail":"patch is not found"}')

    data = {
        "id": app.id,
        "rsa": app.rsa,
        "version": {
            "name": version.name,
            "patch": {
                "id": patch.id,
                "size": patch.size,
                "download_url": patch.download_url
            }
        }
    }
        
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
