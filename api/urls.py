from django.urls import path

from . import vanguard, punch, search, vcoronavirus

app_name='api'

urlpatterns = [
    path('api/vanguard/apikey=<str:apikey>/<str:category>/', vanguard.vanguard, name='vanguard'),
    path('api/punch/apikey=<str:apikey>/<str:category>', punch.punch, name='punch'),
    path('api/search/apikey=<str:apikey>/<str:searchterm>', search.search, name='search'),
    path('api/apikey=<str:apikey>/coronavirus/update', vcoronavirus.vcoronavirus, name='vcoronavirus'),
    
]
