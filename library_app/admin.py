# books/admin.py
from django.contrib import admin
from library_app.models import Author, Genre, Book
from library_app.filters import BookFilter


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'publish_date', 'stock_quantity']
    list_filter = ['author', 'genre', 'publish_date', 'stock_quantity']
    search_fields = ['title', 'author__name', 'genre__name']
    ordering = ['title']
    list_per_page = 20


