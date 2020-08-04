from . models import Profile, Membership, UserMembership, Subscription

from rest_framework import serializers
from django.contrib.auth.models import User



class  UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'id',
            'email',
        
        ]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
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




class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = [
            'membership_type','donation'
        ]

class UserMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    Membership = MembershipSerializer(many=False, read_only=True)
    class Meta:
        model = UserMembership
        fields = [
           'Membership',
           'user',
           'membership'
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'user_membership'
        ]