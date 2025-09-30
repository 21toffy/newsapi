"""
Management command to reset daily usage counters
Run this daily via cron job: 0 0 * * * python manage.py reset_daily_usage
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import APIKey


class Command(BaseCommand):
    help = 'Reset daily usage counters for all API keys'
    
    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Reset all API keys that haven't been reset today
        updated_count = APIKey.objects.filter(
            last_reset_date__lt=today
        ).update(
            daily_requests=0,
            last_reset_date=today
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully reset daily usage for {updated_count} API keys'
            )
        )
