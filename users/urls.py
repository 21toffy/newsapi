from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.profile, name="user_profile"),
    
 

]