
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="9ja News API",
        default_version='v2.0',
        description="Nigeria's single source of truth for news",
        terms_of_service="https://9janewsapi.com.ng/terms/",
        contact=openapi.Contact(email="support@9janews.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API Endpoints
    path('', include('api.urls')),
    path('', include('users.urls')),
]

# Debug Toolbar (Development only)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
