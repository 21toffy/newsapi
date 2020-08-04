from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import string,random
import binascii
import os



class Membership(models.Model):
    MEMBERSHIP_CHOICES = (
    ('Free','free'),
    ('patron', 'Patron')
    )

    slug = models.SlugField(null=True, blank=True)

    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Free',max_length=30)

    donation = models.DecimalField(max_digits=19, decimal_places=3)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(User, related_name='user_membership', on_delete=models.CASCADE)

    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.membership:
            self.membership = 'Free'
        return super(UserMembership, self).save(*args, **kwargs)


    def __str__(self):
       return self.user.username


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE)

    active = models.BooleanField(default=True)

    def __str__(self):
      return self.user_membership.user.username


class Profile(models.Model):
    
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    api_key = models.CharField(max_length=40, primary_key=True)
    is_active = models.BooleanField(default=True)
    no_of_requests = models.PositiveIntegerField(default=0)
    # requests = models.
    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = self.generate_key()
        return super(Profile, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __unicode__(self):
        return self.api_key
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=kwargs.get('instance'))