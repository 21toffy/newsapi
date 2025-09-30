"""
User and API Key views
Clean, production-ready views for API key management
"""
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import APIKey
from .serializers import APIKeySerializer, UsageStatsSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_api_key(request):
    """
    Get user's API key and usage statistics
    """
    try:
        api_key = APIKey.objects.get(user=request.user)
        serializer = APIKeySerializer(api_key)
        return Response(serializer.data)
    except APIKey.DoesNotExist:
        return Response(
            {'error': 'API key not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def regenerate_api_key(request):
    """
    Regenerate user's API key (invalidates the old one)
    """
    try:
        api_key = APIKey.objects.get(user=request.user)
        api_key.key = api_key.generate_key()
        api_key.daily_requests = 0  # Reset usage
        api_key.save()
        
        serializer = APIKeySerializer(api_key)
        return Response({
            'message': 'API key regenerated successfully',
            'api_key': serializer.data
        })
    except APIKey.DoesNotExist:
        return Response(
            {'error': 'API key not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usage_stats(request):
    """
    Get detailed usage statistics for the user
    """
    try:
        api_key = APIKey.objects.get(user=request.user)
        stats = {
            'daily_requests': api_key.daily_requests,
            'daily_limit': api_key.daily_limit,
            'remaining_requests': api_key.get_remaining_requests(),
            'total_requests': api_key.total_requests,
            'last_used': api_key.last_used,
        }
        serializer = UsageStatsSerializer(stats)
        return Response(serializer.data)
    except APIKey.DoesNotExist:
        return Response(
            {'error': 'API key not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_api_key(request):
    """
    Enable/disable API key
    """
    try:
        api_key = APIKey.objects.get(user=request.user)
        api_key.is_active = not api_key.is_active
        api_key.save()
        
        serializer = APIKeySerializer(api_key)
        return Response({
            'message': f'API key {"activated" if api_key.is_active else "deactivated"}',
            'api_key': serializer.data
        })
    except APIKey.DoesNotExist:
        return Response(
            {'error': 'API key not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )