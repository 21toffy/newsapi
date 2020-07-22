from django.urls import path

from . import views

app_name='api'

urlpatterns = [
    path('apis/vanguard/<str:category>', views.vanguard, name='punch'),
    
]
