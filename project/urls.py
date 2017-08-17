"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from api import views as apiviews
from tools import views as toolsviews
from rest_framework_swagger.views import get_swagger_view

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken import views as authviews
from rest_auth.views import PasswordChangeView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categorys', apiviews.CategoryViewSet)
router.register(r'systems', apiviews.SystemViewSet)
router.register(r'apps', apiviews.AppViewSet)
router.register(r'versions', apiviews.VersionViewSet)
router.register(r'patchs', apiviews.PatchViewSet)

schema_view = get_swagger_view(title='Hotfix API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='Hotfix API')),
    url(r'^$', schema_view),
    url(r'^check_update$', apiviews.check_update),
    url(r'^qrcode/(.+)$', toolsviews.generate_qrcode),
    url(r'^password/change$', PasswordChangeView.as_view(), name='rest_password_change'),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    url(r'^api-token-auth/', authviews.obtain_auth_token)
]
