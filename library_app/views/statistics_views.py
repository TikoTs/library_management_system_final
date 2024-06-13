from django.db.models import Count, F
from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from library_app.models import Book, BooksBorrow
from library_app.serializers import (
    TopBooksSerializer,
    LateReturnBooksSerializer,
    LateReturnUsersSerializer,
)


class StatisticsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        last_year = timezone.now() - timezone.timedelta(days=365)

        # Most popular 10 books (the most requested)
        popular_books = Book.objects.annotate(times_borrowed=Count("borrows")).order_by(
            "-times_borrowed"
        )[:10]

        # For each book, how many times it was taken out of the library in the last year
        books_borrowed_last_year = (
            Book.objects.filter(borrows__borrowed_date__gte=last_year)
            .annotate(times_borrowed=Count("borrows"))
            .order_by("-times_borrowed")
        )

        # Top 100 books that users delayed returning most often
        late_books = (
            BooksBorrow.objects.filter(
                borrowed_status="returned",
                return_date__gt=F("borrowed_date") + timezone.timedelta(days=1),
            )
            .values("book__title")
            .annotate(late_returns_count=Count("id"))
            .order_by("-late_returns_count")[:100]
        )

        # Top 100 users who return the book most often late
        late_users = (
            BooksBorrow.objects.filter(
                borrowed_status="returned",
                return_date__gt=F("borrowed_date") + timezone.timedelta(days=1),
            )
            .values("borrower__email")
            .annotate(late_returns_count=Count("id"))
            .order_by("-late_returns_count")[:100]
        )

        data = {
            "popular_books": TopBooksSerializer(popular_books, many=True).data,
            "books_borrowed_last_year": TopBooksSerializer(
                books_borrowed_last_year, many=True
            ).data,
            "late_books": LateReturnBooksSerializer(late_books, many=True).data,
            "late_users": LateReturnUsersSerializer(late_users, many=True).data,
        }
        return Response(data)
