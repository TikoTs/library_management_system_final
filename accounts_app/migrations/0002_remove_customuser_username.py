# Generated by Django 5.0.3 on 2024-05-19 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="username",
        ),
    ]
