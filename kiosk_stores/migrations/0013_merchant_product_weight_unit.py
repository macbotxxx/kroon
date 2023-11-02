# Generated by Django 3.2.9 on 2022-06-13 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_stores', '0012_alter_merchant_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant_product',
            name='weight_unit',
            field=models.CharField(blank=True, help_text='product weight unit i smeant to be inputed by the merchant or the product uploader.', max_length=50, null=True, verbose_name='Weight Unit'),
        ),
    ]