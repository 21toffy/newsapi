"""
User and API Key URLs
Clean URL patterns for API key management
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('api-key/', views.get_api_key, name='get_api_key'),
    path('api-key/regenerate/', views.regenerate_api_key, name='regenerate_api_key'),
    path('api-key/toggle/', views.toggle_api_key, name='toggle_api_key'),
    path('usage-stats/', views.usage_stats, name='usage_stats'),
]