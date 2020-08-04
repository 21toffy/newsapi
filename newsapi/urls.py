
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),

]
