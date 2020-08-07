"""
URL Configuration
"""
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title=" API",
        default_version='v1'
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include('data_capturing_unit.urls'))
]
