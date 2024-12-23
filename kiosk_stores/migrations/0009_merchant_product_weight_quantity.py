# Generated by Django 3.2.9 on 2022-06-01 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_stores', '0008_alter_merchant_product_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant_product',
            name='weight_quantity',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='the stores the product quantity via weight', max_digits=300, null=True, verbose_name='Weight Quantity'),
        ),
    ]
