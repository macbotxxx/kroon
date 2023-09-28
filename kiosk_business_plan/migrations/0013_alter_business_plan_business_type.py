# Generated by Django 3.2.9 on 2022-06-12 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_business_plan', '0012_auto_20220530_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_plan',
            name='business_type',
            field=models.CharField(help_text='gthe merchant need to select the business type on which their business runs on.', max_length=255, null=True, verbose_name='Business Type'),
        ),
    ]
