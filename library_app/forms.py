from django import forms
from library_app.models import Book, BookReservation


class BookReservationForm(forms.ModelForm):
    class Meta:
        model = BookReservation
        fields = ["book"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = Book.objects.filter(stock_quantity__gt=0)
