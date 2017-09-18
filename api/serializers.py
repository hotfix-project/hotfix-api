from .models import Category, System, App, Version, Patch
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class SystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = System
        fields = ('id', 'name')


class AppSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = App
        fields = ('id', 'name', 'category_id', 'system_id', 'key', 'secret', 'rsa')


class VersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Version
        fields = ('id', 'name', 'app_id', 'create_time')


class PatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patch
        fields = (
            'id', 'version_id', 'size', 'desc',
            'download_url', 'md5sum', 'serial_number',
            'status', 'download_count', 'apply_count',
            'pool_size', 'create_time',
        )
