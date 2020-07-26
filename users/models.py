from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import string,random
import binascii
import os



class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    api_key = models.CharField(max_length=40, primary_key=True)
    is_active = models.BooleanField(default=True)
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