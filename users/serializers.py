
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import User, Profile

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
  class Meta(UserCreateSerializer.Meta):
    model = User
    fields = ('id', 'email', 'name', 'password')



class ProfileSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = [
            'pk',
            'bio',
            'api_key',
            'no_of_requests',
            'user'
            ]
        read_only_fields = ['pk', 'api_key']




# class MembershipSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Membership
#         fields = [
#             'membership_type','donation'
#         ]

# class UserMembershipSerializer(serializers.ModelSerializer):
#     user = UserSerializer(many=False, read_only=True)
#     Membership = MembershipSerializer(many=False, read_only=True)
#     class Meta:
#         model = UserMembership
#         fields = [
#            'Membership',
#            'user',
#            'membership'
#         ]


# class SubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = [
#             'user_membership'
#         ]