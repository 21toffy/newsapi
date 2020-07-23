from django.urls import path

from . import vanguard, punch, search

app_name='api'

urlpatterns = [
    path('api/vanguard/<str:category>', vanguard.vanguard, name='vanguard'),
    path('api/punch/<str:category>', punch.punch, name='punch'),
    path('api/search/<str:searchterm>', search.search, name='search'),
    
]
