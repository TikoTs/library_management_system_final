from django.db.models import Count, F
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.utils import timezone
from django.db import transaction

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
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["author", "genre"]
    search_fields = ["title", "author__name", "genre__name"]
    ordering_fields = ["demand"]
    pagination_class = None  # Django's default pagination
    ordering = ["-demand"]  # Default ordering will be by demand
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Book.objects.all().annotate(demand=Count("borrows")).order_by("-demand")


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
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class AvailableBookTitlesView(generics.ListAPIView):
    queryset = Book.objects.filter(stock_quantity__gt=0)
    serializer_class = AvailableBookTitleSerializer
    permission_classes = [IsAuthenticated]


# class BookReservationView(CreateView):
#     model = BookReservation
#     form_class = BookReservationForm
#     template_name = 'templates/library/book_reservation_form.html'
#     success_url = reverse_lazy("book-list")
#
#     def form_valid(self, form):
#         form.instance.borrower = self.request.user
#         return super().form_valid(form)


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
            book.save(update_fields=["stock_quantity"])

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
        borrow.book.save(update_fields=["stock_quantity"])
        borrow.save(update_fields=["borrowed_status", "return_date"])
        return Response(
            {"status": "Book returned successfully"}, status=status.HTTP_200_OK
        )


class BookRequestCreateView(generics.CreateAPIView):
    queryset = BooksBorrow.objects.all()
    serializer_class = BooksBorrowSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")
        book = Book.objects.get(id=book_id)

        if book.stock_quantity > 0:
            return Response(
                {"error": "Book is available, no need to request."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request_instance = BooksBorrow.objects.create(
            book=book,
            borrower=request.user,
            borrowed_status="requested",
        )

        serializer = self.get_serializer(request_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)