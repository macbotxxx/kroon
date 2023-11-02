# Generated by Django 3.2.9 on 2022-04-01 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0071_auto_20220328_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='pending_duration',
            field=models.DateTimeField(blank=True, help_text='duration of which the pending topup will be expired if no action is not been taken.', null=True, verbose_name='Pending Topup Duration'),
        ),
    ]