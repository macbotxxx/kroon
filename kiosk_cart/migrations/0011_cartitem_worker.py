# Generated by Django 3.2.9 on 2022-05-16 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_cart', '0010_payment_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='worker',
            field=models.CharField(blank=True, help_text='this store the workers name that checkout the products for the particular store', max_length=250, null=True, verbose_name='Worker'),
        ),
    ]
