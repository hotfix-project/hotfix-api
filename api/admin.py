from django.contrib import admin

from .models import System, Category, App, Version, Patch
from rest_framework.authtoken.admin import TokenAdmin



class SystemAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']

    def get_ordering(self, request):
        return ['name']

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']

    def get_ordering(self, request):
        return ['name']

class AppAdmin(admin.ModelAdmin):
    fields = ['name', 'category_id', 'system_id', 'key', 'secret', 'rsa']
    list_display = ('name', 'category_id', 'system_id', 'key', 'secret')
    list_filter = [
        'category_id',
        'system_id',
        'name', 
    ]
    search_fields = ['name']

    def get_ordering(self, request):
        return ['name']

class VersionAdmin(admin.ModelAdmin):
    fields = ['name', 'app_id']
    list_display = ('name', 'app_id', 'create_time')
    list_filter = [
        'app_id__name',
        'name', 
        'create_time',
    ]
    search_fields = ['name']

    def get_ordering(self, request):
        return ['name']

class PatchAdmin(admin.ModelAdmin):
    fields = [
        'version_id', 'size', 'desc', 'download_url',
        'serial_number', 'is_enable', 'download_count', 
        'apply_count', 'is_gray', 'pool_size'
    ]
    list_display = (
        'version_id', 'size', 'desc', 'serial_number', 
        'is_enable', 'is_gray', 'create_time', 'update_time'
    )
    list_filter = [
        'version_id__name',
        'size', 
        'create_time', 
        'update_time',
    ]
    search_fields = ['serial_number']


admin.site.register(System, SystemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(App, AppAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Patch, PatchAdmin)

TokenAdmin.raw_id_fields = ('user',)
