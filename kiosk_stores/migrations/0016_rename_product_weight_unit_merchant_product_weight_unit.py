# Generated by Django 3.2.9 on 2022-06-13 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_stores', '0015_rename_weight_unit_merchant_product_product_weight_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='merchant_product',
            old_name='product_weight_unit',
            new_name='weight_unit',
        ),
    ]