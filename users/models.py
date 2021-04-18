from django.db import models
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
import string,random
import binascii
import os




from django.contrib.auth.models import (
  AbstractBaseUser, PermissionsMixin, BaseUserManager)


class UserAccountManager(BaseUserManager):
  
  def create_user(self, email, name, password=None):
    if not email:
      raise ValueError('Usuários precisam fornecer um email')

    email = self.normalize_email(email)
    user = self.model(email=email, name=name)

    user.set_password(password)
    user.save()

    return user


  # def create_superuser():
  #   pass


class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255,)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserAccountManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name',]

  def get_full_name(self):
    return self.name

  def get_short_name(self):
    return self.name


  def __str__(self):
    return self.email

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