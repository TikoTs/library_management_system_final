# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from library_app.views import (
#     AuthorViewSet, GenreViewSet, BookViewSet,
#     BookCreateAPIView, BookUpdateAPIView,
#     BookListView, #BookDetailView,
#     # BookReservationCreateView, BooksBorrowUpdateView,
#     # AvailableBooksListView, BookReservationView
# )
#
# router = DefaultRouter()
# router.register(r'authors', AuthorViewSet)
# router.register(r'genres', GenreViewSet)
# router.register(r'books', BookViewSet)
#
# urlpatterns = [
#     path('', include(router.urls)),
#     path('books/list/', BookListView.as_view(), name='book-list'),
#     path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
#     path('books/create/', BookCreateAPIView.as_view(), name='book-create'),
#     path('books/<int:pk>/update/', BookUpdateAPIView.as_view(), name='book-update'),
#     # path('books/reserve/', BookReservationCreateView.as_view(), name='book-reserve'),
#     # path('books/borrow/<int:pk>/return/', BooksBorrowUpdateView.as_view(), name='book-return'),
#     # path('books/available/', AvailableBooksListView.as_view(), name='available-books'),
#     # path('books/reserve/form/', BookReservationView.as_view(), name='book-reserve-form'),
# ]
