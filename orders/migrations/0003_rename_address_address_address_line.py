# Generated by Django 5.1.3 on 2024-11-28 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_shipping_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address',
            new_name='address_line',
        ),
    ]
