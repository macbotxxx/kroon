# Generated by Django 3.2.9 on 2022-11-10 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kroon_token', '0018_withdrawtokenfees_withdrawal_fee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchasetokenfees',
            old_name='kroon_trasfer_rate',
            new_name='kroon_transfer_rate',
        ),
    ]
