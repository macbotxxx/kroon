# Generated by Django 3.2.9 on 2021-12-14 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_kroontokentransfer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='amount_in_user_default_currency',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='user_default_currency',
        ),
    ]
