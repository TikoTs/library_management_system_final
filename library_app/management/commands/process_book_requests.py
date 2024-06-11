from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from library_app.models import BooksBorrow, Book


class Command(BaseCommand):
    help = "Process book requests and notify users when a book becomes available"

    def handle(self, *args, **kwargs):
        requested_borrows = BooksBorrow.objects.filter(
            borrowed_status="requested", notified=False
        ).select_related("book", "borrower")

        for borrow in requested_borrows:
            if borrow.book.stock_quantity > 0:
                subject = "Book Available for Checkout"
                message = (
                    f"Dear {borrow.borrower.full_name},\n\n"
                    f'The book "{borrow.book.title}" you requested is now available for checkout.\n\n'
                    f"Thank you!"
                )
                recipient_list = [borrow.borrower.email]

                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

                borrow.notified = True
                borrow.save(update_fields=["notified"])

        self.stdout.write(
            self.style.SUCCESS("Processed all book requests and notified users.")
        )
