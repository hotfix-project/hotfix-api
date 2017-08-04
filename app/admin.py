from django.contrib import admin

from .models import System, Category, App


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
    list_display = ('name', 'category_id', 'system_id', 'key', 'secret', 'rsa')
    list_filter = ['name', 'category_id', 'system_id']
    search_fields = ['name']

    def get_ordering(self, request):
        return ['name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        pass

admin.site.register(System, SystemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(App, AppAdmin)
