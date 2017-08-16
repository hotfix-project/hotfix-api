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
    version = request.GET.get('version')
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
        selected = (Patch.STATUS_RELEASED, Patch.STATUS_PRERELEASED, Patch.STATUS_DELETED)
        patchs = Patch.objects.filter(id=version.id, status__in=selected)
    except Patch.DoesNotExist:
        return HttpResponseNotFound('{"detail":"patch is not found"}')

    data = {
        "id": app.id,
        "version": version.name,
        "rsa": app.rsa,
        "results": {
            "released": list(patchs.filter(
                status=Patch.STATUS_RELEASED).values(
                    'id', 'version_id', 'status', 'download_url')),
            "prereleased": list(patchs.filter(
                status=Patch.STATUS_PRERELEASED).filter(pool_size__gt=0).values(
                    'id', 'version_id', 'status', 'download_url')),
            "deleted": list(patchs.filter(
                status=Patch.STATUS_DELETED).values('id', 'version_id')),
        }
    }

    for patch in patchs:
        if patch.status == Patch.STATUS_PRERELEASED and patch.pool_size > 0:
            patch.pool_size = patch.pool_size - 1
            patch.save()
        
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
