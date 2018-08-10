"""OfficeCafe URL Configuration

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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


admin.site.site_header = "OfficeCafe Administration | By CMT"
admin.site.site_title = "OfficeCafe Administration | By CMT"

schema_view = get_schema_view(
   openapi.Info(
      title="OfficeCafe API",
      default_version='v1',
      description="API based on DRF YASG for OfficeCafe",
      #terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="admin@officecafe.in"),
      license=openapi.License(name="BSD License"),
   ),
   #validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^admin/', admin.site.urls),
    url(r'^api/restaurant/', include('restaurant.urls')),
    url(r'^api/billing/', include('billing.urls')),
    url(r'^api/users/', include('drf_user.urls')),
    url(r'^api/instamojo/', include('drf_instamojo.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]
