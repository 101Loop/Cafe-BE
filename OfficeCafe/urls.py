"""OfficeCafe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path(^blog/', include('blog.urls'))
"""

from django.urls import re_path, path, include
from django.contrib import admin

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions


admin.site.site_header = "OfficeCafe Administration"
admin.site.site_title = "OfficeCafe Administration"

schema_view = get_schema_view(
    openapi.Info(
        title="OfficeCafe API",
        default_version='v1',
        description="API based on DRF YASG for OfficeCafe",
        contact=openapi.Contact(email="admin@officecafe.in"),
        license=openapi.License(name="BSD License"),
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui('cache_timeout=None'), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=None),
         name='schema-redoc'),

    path('api/users/', include('drf_user.urls')),
    path('api/instamojo/', include('drf_instamojo.urls')),
    path('api/outlet/', include('outlet.urls')),
    path('api/location/', include('location.urls')),
    path('api/product/', include('product.urls')),
    path('api/order/', include('order.urls')),

    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('', admin.site.urls),
]
