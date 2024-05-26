from django.db.models import Count, F
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from django.utils import timezone
from django.db import transaction
from rest_framework.views import APIView

from library_app.forms import BookReservationForm
from library_app.models import Author, Genre, Book, BookReservation, BooksBorrow
from library_app.serializers import (
    AuthorSerializer,
    GenreSerializer,
    BookSerializer,
    BookDetailSerializer,
    BookCreateSerializer,
    BookUpdateSerializer,
    BookReservationSerializer,
    BooksBorrowSerializer,
    BookReservationCreateSerializer,
    AvailableBookTitleSerializer,
    LateReturnBooksSerializer,
    TopBooksSerializer,
    LateReturnUsersSerializer,
)
from library_app.permissions import IsLibrarian


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["author", "genre"]
    search_fields = ["title", "author__name", "genre__name"]
    pagination_class = None  # Django's default pagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]


class BookUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookUpdateSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]


class AllBooksListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class AvailableBookTitlesView(generics.ListAPIView):
    queryset = Book.objects.filter(stock_quantity__gt=0)
    serializer_class = AvailableBookTitleSerializer
    permission_classes = [IsAuthenticated]


class BookReservationView(CreateView):
    model = BookReservation
    form_class = BookReservationForm
    template_name = "templates/library/book_reservation_form.html"
    success_url = reverse_lazy("book-list")

    def form_valid(self, form):
        form.instance.borrower = self.request.user
        return super().form_valid(form)


class BookReservationCreateView(generics.CreateAPIView):
    queryset = BookReservation.objects.all()
    serializer_class = BookReservationCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get("book")
        book = Book.objects.get(id=book_id)

        if book.stock_quantity < 1:
            return Response(
                {"error": "Book not available in stock"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            book.stock_quantity -= 1
            book.save()

            reservation = BookReservation.objects.create(
                book=book,
                borrower=user,
                reservation_status="reserved",
                expiration_date=timezone.now() + timezone.timedelta(days=1),
            )
            serializer = self.get_serializer(reservation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class BooksBorrowUpdateView(generics.UpdateAPIView):
    queryset = BooksBorrow.objects.all()
    serializer_class = BooksBorrowSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]

    def update(self, request, *args, **kwargs):
        borrow = self.get_object()
        borrow.borrowed_status = "returned"
        borrow.return_date = timezone.now()
        borrow.book.stock_quantity += 1
        borrow.book.save()
        borrow.save()
        return Response(
            {"status": "Book returned successfully"}, status=status.HTTP_200_OK
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
