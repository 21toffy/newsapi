from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from .models import User, Profile
from .serializers import UserCreateSerializer, ProfileSerializer
from .models import User






@api_view([ 'GET'])
def profile(request):
    if request.method == 'GET':
        #current user online
        try:
            current_user = request.user.pk
            print(request.user.pk)
            me = User.objects.get(pk=current_user)
           
        except user.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # profile of current user online
        data = Profile.objects.get(user=me)
        serializer = ProfileSerializer(data)
        
        #number of listing of a user
        # current_membership =Listing.objects.filter(realtor=user).count()
        # serializer2 =UserMembershipSerializer(user_membership_qs)

        # result = {'serializer2':serializer2.data, 'serializer':serializer.data}
        result = {'serializer':serializer.data}


        # return Response(serializer.data)

        return Response(result)


