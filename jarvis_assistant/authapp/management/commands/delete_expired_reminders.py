from django.core.management.base import BaseCommand
from django.utils import timezone
from authapp.models import Reminder

class Command(BaseCommand):
    help = 'Delete reminders that are overdue by more than 2 days'

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timezone.timedelta(days=2)
        expired_reminders = Reminder.objects.filter(due_date__lt=cutoff_date)
        expired_count = expired_reminders.count()
        expired_reminders.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {expired_count} expired reminders'))
