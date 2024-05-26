from django.core.management.base import BaseCommand
from library_app.models import BookReservation
from django.utils import timezone


class Command(BaseCommand):
    help = "Remove expired book reservations"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_reservations = BookReservation.objects.filter(
            expiration_date__lt=now, reservation_status="reserved"
        )

        for reservation in expired_reservations:
            reservation.book.quantity_in_stock += 1
            reservation.book.save()
            reservation.delete()

        self.stdout.write(
            self.style.SUCCESS("Successfully removed expired reservations")
        )
