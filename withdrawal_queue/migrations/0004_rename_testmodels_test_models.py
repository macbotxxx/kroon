# Generated by Django 3.2.9 on 2022-03-31 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdrawal_queue', '0003_alter_testmodels_content'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestModels',
            new_name='Test_Models',
        ),
    ]
