# Generated by Django 3.2.9 on 2022-04-01 23:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0072_payment_pending_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='pending_duration',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='duration of which the pending topup will be expired if no action is not been take.', null=True, verbose_name='Pending Topup Duration'),
        ),
    ]
