from django.contrib import admin
from library_app.models import Author, Genre, Book, BookReservation, BooksBorrow


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class BooksBorrowInline(admin.TabularInline):
    model = BooksBorrow
    extra = 0
    readonly_fields = ("borrower", "borrowed_date", "return_date", "borrowed_status")


class BookReservationInline(admin.TabularInline):
    model = BookReservation
    extra = 0
    readonly_fields = (
        "borrower",
        "reserved_date",
        "expiration_date",
        "reservation_status",
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "genre",
        "publish_date",
        "stock_quantity",
        "issued_count",
        "total_books_published",
    ]
    list_filter = ["author", "genre", "publish_date", "stock_quantity"]
    search_fields = ["title", "author__name", "genre__name"]
    ordering = ["title"]
    list_per_page = 20
    inlines = [BooksBorrowInline, BookReservationInline]
    readonly_fields = ("issued_count", "total_books_published")

    def issued_count(self, obj):
        return obj.borrows.filter(borrowed_status="borrowed").count()

    issued_count.short_description = "Times Issued"

    def total_books_published(self, obj):
        return Book.objects.count()

    total_books_published.short_description = "Total Books Published"
