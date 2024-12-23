# Generated by Django 3.2.9 on 2022-04-18 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0073_alter_payment_pending_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='service_providers',
            field=models.CharField(blank=True, help_text='this stores the Service Provider of which the customer used while making payment', max_length=255, null=True, verbose_name='Service Provider'),
        ),
    ]
