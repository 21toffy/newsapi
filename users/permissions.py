from rest_framework import permissions
from .models import Profile


class OnlyAPIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            api_key = request.QUERY_PARAMS.get('apikey', False)
            print(api_key)
            Profile.objects.get(api_key=api_key)
            return True
        except:
            return False

