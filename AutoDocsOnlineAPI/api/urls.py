from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter as Router

from .views import (
    DocumentViewSet,
    DocumentsPackageViewSet,
    TemplateViewSet,
    UserDefaultTemplateValueViewSet,
)


router = Router()
router.register('documents', DocumentViewSet, 'documents')
router.register('templates', TemplateViewSet, 'templates')
router.register(
    'default_templates_values',
    UserDefaultTemplateValueViewSet,
    'default_templates_values'
)
router.register(
    'documents_packages',
    DocumentsPackageViewSet,
    'documents_packages'
)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls'))
]

schema_view = get_schema_view(
    openapi.Info(
        title="Docs API",
        default_version='v1',
        description="Documentation",
        # terms_of_service="URL страницы с пользовательским соглашением",
        contact=openapi.Contact(email="zaliznuak50@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
