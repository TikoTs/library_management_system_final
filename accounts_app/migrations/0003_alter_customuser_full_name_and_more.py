# Generated by Django 5.0.3 on 2024-05-19 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts_app", "0002_remove_customuser_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="full_name",
            field=models.CharField(max_length=300, verbose_name="full name"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="personal_number",
            field=models.CharField(max_length=11, verbose_name="personal number"),
        ),
    ]