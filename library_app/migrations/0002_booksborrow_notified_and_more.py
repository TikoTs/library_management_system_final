# Generated by Django 5.0.3 on 2024-06-10 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booksborrow",
            name="notified",
            field=models.BooleanField(default=False, verbose_name="Notified"),
        ),
        migrations.AlterField(
            model_name="booksborrow",
            name="borrowed_status",
            field=models.CharField(
                choices=[
                    ("borrowed", "Borrowed"),
                    ("returned", "Returned"),
                    ("requested", "Requested"),
                ],
                default="borrowed",
                max_length=50,
                verbose_name="Borrowed Status",
            ),
        ),
    ]
