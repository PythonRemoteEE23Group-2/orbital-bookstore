# Generated by Django 5.1 on 2024-10-03 11:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0007_remove_book_category_remove_cart_book_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, default="", max_length=150),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, default="", max_length=150),
        ),
    ]