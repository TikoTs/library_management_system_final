from .models import Author, Book
from faker import Faker
import baker

fake = Faker()


def create_author():
    return baker.make(
        Author,
        name=fake.name(),
        birthdate=fake.date_of_birth(minimum_age=25, maximum_age=90)
    )


author = create_author()
print(author.name, author.birthdate)
