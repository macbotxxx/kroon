# Generated by Django 3.2.9 on 2022-05-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_stores', '0005_auto_20220512_2322'),
        ('kiosk_cart', '0005_alter_payment_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='product_variation',
            field=models.ManyToManyField(blank=True, to='kiosk_stores.ProductVariation'),
        ),
    ]
