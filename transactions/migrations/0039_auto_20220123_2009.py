# Generated by Django 3.2.9 on 2022-01-23 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0038_kroontokenrequest_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='action',
            field=models.CharField(default='KROON WALLET TOPUP', help_text='The payment action for the current transaction.', max_length=150, null=True, verbose_name='Payment Method'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(default='ONLINE PAYMENT', help_text='The payment method used while paying for an order.', max_length=150, null=True, verbose_name='Payment Method'),
        ),
    ]
