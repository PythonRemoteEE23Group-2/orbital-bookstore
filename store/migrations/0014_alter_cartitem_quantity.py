# Generated by Django 5.1 on 2024-10-05 14:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0013_remove_order_email_sent_date_cartitem_order_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
