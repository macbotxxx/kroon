# Generated by Django 3.2.9 on 2022-03-29 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdrawal_queue', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testmodels',
            options={'ordering': ('-created_date',)},
        ),
    ]
