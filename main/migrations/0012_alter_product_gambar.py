# Generated by Django 4.2.5 on 2024-10-24 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_cart_email_cart_name_cart_phone_number_cart_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='gambar',
            field=models.URLField(),
        ),
    ]
