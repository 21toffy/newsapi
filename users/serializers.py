from . models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = [
            'pk',
            'bio',
            'api_key',
            'user',
            ]
        read_only_fields = ['pk', 'api_key']