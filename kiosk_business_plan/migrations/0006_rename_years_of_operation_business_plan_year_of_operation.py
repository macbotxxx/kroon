# Generated by Django 3.2.9 on 2022-05-28 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_business_plan', '0005_auto_20220528_1741'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business_plan',
            old_name='years_of_operation',
            new_name='year_of_operation',
        ),
    ]
