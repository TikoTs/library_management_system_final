from library_app.views.views import (
    AuthorViewSet,
    GenreViewSet,
    BookListView,
    BookDetailView,
    BookCreateAPIView,
    BookUpdateAPIView,
    AllBooksListView,
    AvailableBookTitlesView,
    BookReservationCreateView,
    BooksBorrowUpdateView,
    BookRequestCreateView,
)
from library_app.views.statistics_views import StatisticsAPIView

__all__ =[
    "AuthorViewSet",
    "GenreViewSet",
    "BookListView",
    "BookDetailView",
    "BookCreateAPIView",
    "BookUpdateAPIView",
    "AllBooksListView",
    "AvailableBookTitlesView",
    "BookReservationCreateView",
    "BooksBorrowUpdateView",
    "BookRequestCreateView",
    "StatisticsAPIView",
]
