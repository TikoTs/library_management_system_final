from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings


class Author(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("Author Name"),
        unique=True,
        default="Unknown Author",
    )
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("Genre Name"),
        unique=True,
        default="Unknown Genre",
    )
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=255, null=False, blank=False, verbose_name=_("Title")
    )
    author = models.ForeignKey(
        Author, verbose_name=_("Author"), on_delete=models.CASCADE
    )
    genre = models.ForeignKey(Genre, verbose_name=_("Genre"), on_delete=models.CASCADE)
    publish_date = models.DateField(
        verbose_name=_("Date of Publish"), default=timezone.now
    )
    stock_quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity of Stock"), default=0
    )

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title

    def issued_count(self):
        return self.borrows.filter(borrowed_status="borrowed").count()


class BookReservation(models.Model):
    book = models.ForeignKey(
        Book,
        related_name="reservations",
        verbose_name=_("Book"),
        on_delete=models.CASCADE,
    )
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reservations",
        verbose_name=_("Borrower"),
        on_delete=models.CASCADE,
    )
    reserved_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Reserved Date"),
        help_text=_("Creates automatically"),
    )
    expiration_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expiration Date"),
        help_text=_("Date/time when reservation expires"),
    )
    reservation_status = models.CharField(
        max_length=50,
        choices=[("reserved", "Reserved"), ("picked_up", "Picked Up")],
        default="reserved",
        verbose_name=_("Reservation Status"),
    )

    class Meta:
        verbose_name = _("Book Reservation")
        verbose_name_plural = _("Book Reservations")
        ordering = ["-reserved_date"]

    def save(self, *args, **kwargs):
        if not self.expiration_date and self.reservation_status == "reserved":
            self.expiration_date = timezone.now() + timezone.timedelta(days=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} - {self.borrower.email} | {self.reserved_date}"

    @transaction.atomic
    def process_pickup(self):
        if self.reservation_status == "reserved":
            self.reservation_status = "picked_up"
            self.save()

            borrow = BooksBorrow.objects.create(
                book=self.book, borrower=self.borrower, borrowed_status="borrowed"
            )

            self.borrow = borrow
            self.save()


class BooksBorrow(models.Model):
    book = models.ForeignKey(
        Book, related_name="borrows", verbose_name=_("Book"), on_delete=models.CASCADE
    )
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="borrows",
        verbose_name=_("Borrower"),
        on_delete=models.CASCADE,
    )
    borrowed_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Borrowed Date"),
        help_text=_("Creates automatically"),
    )
    borrowed_status = models.CharField(
        max_length=50,
        choices=[("borrowed", "Borrowed"), ("returned", "Returned")],
        default="borrowed",
        verbose_name=_("Borrowed Status"),
    )
    return_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Return Date"),
        help_text=_("Date/time of returning borrowed book"),
    )

    class Meta:
        verbose_name = _("Books Borrow")
        verbose_name_plural = _("Books Borrows")
        ordering = ["-borrowed_date"]

    def __str__(self):
        return f"{self.book.title} - {self.borrower.email} | {self.borrowed_date}"
