from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from library_app.models import BooksBorrow


class Command(BaseCommand):
    help = 'Send reminder emails for overdue books and update their status'

    def handle(self, *args, **kwargs):
        now = timezone.now() - timezone.timedelta(days=14)
        expired_borrows = BooksBorrow.objects.filter(
            borrowed_status='borrowed',
            borrowed_date__lt=now
        )

        if not expired_borrows.exists():
            self.stdout.write(self.style.SUCCESS('No expired reservations found.'))
            return

        with transaction.atomic():
            for borrow in expired_borrows:
                borrow.borrowed_status = 'overdue'
                borrow.save(update_fields=['borrowed_status'])

                subject = 'Your borrowed book is overdue'
                message = (
                    f'Dear {borrow.borrower.full_name},\n\n'
                    f'Your borrowed book "{borrow.book.title}" is now overdue. '
                    f'Please return it as soon as possible.\n\n'
                )
                recipient_list = [borrow.borrower.email]

                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        self.stdout.write(self.style.SUCCESS('Successfully sent overdue reminders and updated book status.'))
