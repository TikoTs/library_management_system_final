import django_filters
from library_app.models import Book


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            "title": ["icontains"],
            "author__name": ["icontains"],
            "genre__name": ["exact"],
            "publish_date": ["year__gte", "year__lte"],
            "stock_quantity": ["gte", "lte"],
        }
