
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('api.urls')),
    path('', include('users.urls')),
    path('api/v1/', include('users.urls')),

    # path('rest-auth/', include('rest_auth.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
