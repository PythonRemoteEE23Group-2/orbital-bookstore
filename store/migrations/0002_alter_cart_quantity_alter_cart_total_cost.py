from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),  # Eelmine migratsioonifail
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),  # Siin muudetakse quantity tüüpi või vaikeväärtust
        ),
    ]
