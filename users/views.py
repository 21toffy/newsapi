from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Profile, Membership, UserMembership, Subscription

from .serializers import ProfileSerializer, UserSerializer, MembershipSerializer, UserMembershipSerializer, SubscriptionSerializer





@api_view([ 'GET'])
def profile(request, username):
    if request.method == 'GET':
        #current user online
        try:
            user = User.objects.get(username=username)

            user_membership_qs = UserMembership.objects.filter(user=request.user).first()          
            # current_membership = str(user_membership_qs.membership)
            
            
        except user.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # profile of current user online
        data = Profile.objects.get(user=user)
        serializer = ProfileSerializer(data)
        
        #number of listing of a user
        # current_membership =Listing.objects.filter(realtor=user).count()
        serializer2 =UserMembershipSerializer(user_membership_qs)

        result = {'serializer2':serializer2.data, 'serializer':serializer.data}
        # result = {'serializer':serializer.data}


        # return Response(serializer.data)

        return Response(result)


