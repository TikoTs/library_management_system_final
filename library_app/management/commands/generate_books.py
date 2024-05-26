import os
import django
import random
from faker import Faker
from django.core.management.base import BaseCommand
from library_app.models import Author, Book, Genre


class Command(BaseCommand):
    help = "Populate the database with random books"

    def handle(self, *args, **kwargs):
        fake = Faker()

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_management.settings")
        django.setup()

        # Clear existing data
        Book.objects.all().delete()
        Author.objects.all().delete()
        Genre.objects.all().delete()

        authors = []
        for _ in range(100):
            author = Author.objects.create(name=fake.name(), description=fake.text())
            authors.append(author)

        genre_names = [
            "Science Fiction",
            "Fantasy",
            "Mystery",
            "Thriller",
            "Romance",
            "Non-fiction",
            "Horror",
            "Biography",
        ]
        genres = []
        for name in genre_names:
            genre = Genre.objects.create(name=name, description=fake.text())
            genres.append(genre)

        for _ in range(1000):
            book = Book.objects.create(
                title=fake.sentence(nb_words=4),
                author=random.choice(authors),
                genre=random.choice(genres),
                publish_date=fake.date_between(start_date="-30y", end_date="today"),
                stock_quantity=random.randint(1, 20),
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with books")
        )
