# Generated by Django 3.2.9 on 2022-02-24 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kroon_kyc', '0008_auto_20220224_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marchantkycapplication',
            name='registered_ip_address',
        ),
    ]
