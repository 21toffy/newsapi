"""
Serializers for User and API Key models
Clean, production-ready serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import APIKey, UsageLog

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for profile information"""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class APIKeySerializer(serializers.ModelSerializer):
    """API Key serializer with usage information"""
    user = UserSerializer(read_only=True)
    remaining_requests = serializers.SerializerMethodField()
    
    class Meta:
        model = APIKey
        fields = (
            'key', 'is_active', 'created_at', 'last_used',
            'daily_requests', 'daily_limit', 'total_requests',
            'remaining_requests', 'user'
        )
        read_only_fields = (
            'key', 'created_at', 'last_used', 'daily_requests', 
            'total_requests', 'user'
        )
    
    def get_remaining_requests(self, obj):
        """Get remaining requests for today"""
        return obj.get_remaining_requests()


class UsageStatsSerializer(serializers.Serializer):
    """Serializer for usage statistics"""
    daily_requests = serializers.IntegerField()
    daily_limit = serializers.IntegerField()
    remaining_requests = serializers.IntegerField()
    total_requests = serializers.IntegerField()
    last_used = serializers.DateTimeField()


# Optional: Usage log serializer for analytics
class UsageLogSerializer(serializers.ModelSerializer):
    """Usage log serializer for detailed analytics"""
    
    class Meta:
        model = UsageLog
        fields = (
            'endpoint', 'timestamp', 'ip_address', 
            'user_agent', 'response_time_ms'
        )
        read_only_fields = ('timestamp',)