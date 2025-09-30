"""
User and API Key models for 9ja News API
Production-grade, scalable design for free API service
"""
import secrets
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import EmailValidator
from django.db.models import F
from common.models import BaseModel
from .managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with email as username
    Optimized for API service with minimal fields
    """
    email = models.EmailField(
        max_length=255, 
        unique=True,
        validators=[EmailValidator()],
        db_index=True
    )
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name


class APIKey(BaseModel):
    """
    API Key model - One key per user for simplicity
    Optimized for high-frequency lookups and updates
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='api_key'
    )
    key = models.CharField(
        max_length=40, 
        unique=True, 
        db_index=True,
        help_text="40-character hexadecimal API key"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Usage tracking
    total_requests = models.PositiveIntegerField(default=0)
    daily_requests = models.PositiveIntegerField(default=0)
    last_reset_date = models.DateField(default=timezone.now)
    
    # Rate limiting (requests per day for free tier)
    daily_limit = models.PositiveIntegerField(default=1000)
    
    class Meta:
        db_table = 'api_keys'
        indexes = [
            models.Index(fields=['key']),  # Primary lookup index
            models.Index(fields=['user']),
            models.Index(fields=['is_active']),
            models.Index(fields=['last_reset_date']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)
    
    def generate_key(self):
        """Generate a secure 40-character hexadecimal API key"""
        return secrets.token_hex(20)
    
    def reset_daily_usage(self):
        """Reset daily usage counter - called by daily cron job"""
        today = timezone.now().date()
        if self.last_reset_date < today:
            self.daily_requests = 0
            self.last_reset_date = today
            self.save(update_fields=['daily_requests', 'last_reset_date'])
    
    def increment_usage(self):
        """
        Increment usage counters atomically
        Returns True if request is allowed, False if limit exceeded
        """
        today = timezone.now().date()
        
        # Reset daily counter if it's a new day
        if self.last_reset_date < today:
            self.daily_requests = 0
            self.last_reset_date = today
        
        # Check if daily limit exceeded
        if self.daily_requests >= self.daily_limit:
            return False
        
        # Atomic increment to prevent race conditions
        APIKey.objects.filter(pk=self.pk).update(
            daily_requests=F('daily_requests') + 1,
            total_requests=F('total_requests') + 1,
            last_used=timezone.now(),
            last_reset_date=today
        )
        
        # Refresh from database
        self.refresh_from_db(fields=['daily_requests', 'total_requests', 'last_used'])
        return True
    
    def get_remaining_requests(self):
        """Get remaining requests for today"""
        return max(0, self.daily_limit - self.daily_requests)
    
    def __str__(self):
        return f"{self.user.email} - {self.key[:8]}..."


# Optional: Usage analytics model for detailed tracking
class UsageLog(BaseModel):
    """
    Optional: Detailed usage logging for analytics
    Comment out if not needed to reduce database load
    """
    api_key = models.ForeignKey(
        APIKey, 
        on_delete=models.CASCADE,
        related_name='usage_logs'
    )
    endpoint = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'usage_logs'
        indexes = [
            models.Index(fields=['api_key', 'timestamp']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['endpoint']),
        ]
        # Partition by date for better performance (PostgreSQL)
        # Consider implementing table partitioning for high volume
    
    def __str__(self):
        return f"{self.api_key.user.email} - {self.endpoint} - {self.timestamp}"


# Signal to automatically create API key when user is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_api_key(sender, instance, created, **kwargs):
    """Automatically create API key when user is created"""
    if created:
        APIKey.objects.create(user=instance)