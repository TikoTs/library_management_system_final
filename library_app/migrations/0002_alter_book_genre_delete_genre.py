# Generated by Django 5.0.3 on 2024-05-24 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="genre",
            field=models.CharField(
                choices=[
                    ("FICTION", "Fiction"),
                    ("NONFICTION", "Non-Fiction"),
                    ("SCIFI", "Science Fiction"),
                    ("FANTASY", "Fantasy"),
                    ("MYSTERY", "Mystery"),
                    ("ROMANCE", "Romance"),
                    ("HORROR", "Horror"),
                ],
                max_length=50,
            ),
        ),
        migrations.DeleteModel(
            name="Genre",
        ),
    ]
