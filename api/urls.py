from django.urls import path

from . import vanguard, punch

app_name='api'

urlpatterns = [
    path('apis/vanguard/<str:category>', vanguard.vanguard, name='vanguard'),
    path('apis/punch/<str:category>', punch.punch, name='punch'),
    
]
