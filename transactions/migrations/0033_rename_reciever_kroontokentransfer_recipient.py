# Generated by Django 3.2.9 on 2022-01-23 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0032_auto_20220123_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kroontokentransfer',
            old_name='reciever',
            new_name='recipient',
        ),
    ]
