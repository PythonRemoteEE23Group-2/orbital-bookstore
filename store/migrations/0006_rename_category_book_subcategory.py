# Generated by Django 5.1.1 on 2024-10-12 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_subcategory_book_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='category',
            new_name='subcategory',
        ),
    ]
