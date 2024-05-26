# library_app/urls.py
from django.urls import path
from library_app.views import AuthorViewSet, GenreViewSet, BookViewSet, BookCreateAPIView, BookUpdateAPIView, \
    BookListView, BookDetailView, BookReservationCreateView, BooksBorrowUpdateView, AvailableBooksListView, \
    AvailableBookTitlesView

urlpatterns = [
    path('authors/', AuthorViewSet.as_view({'get': 'list', 'post': 'create'}), name='author-list'),
    path('authors/<int:pk>/', AuthorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='author-detail'),
    path('genres/', GenreViewSet.as_view({'get': 'list', 'post': 'create'}), name='genre-list'),
    path('genres/<int:pk>/', GenreViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='genre-detail'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateAPIView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateAPIView.as_view(), name='book-update'),
    path('books/reserve/', BookReservationCreateView.as_view(), name='book-reserve'),
    path('books/borrow/<int:pk>/return/', BooksBorrowUpdateView.as_view(), name='book-return'),
    path('books/available/', AvailableBooksListView.as_view(), name='available-books'),
    path('books/available-titles/', AvailableBookTitlesView.as_view(), name='available-book-titles')
]
