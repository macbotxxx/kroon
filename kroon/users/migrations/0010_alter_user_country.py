# Generated by Django 3.2.9 on 2021-12-12 23:41

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20211212_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(help_text='The resisdent country of the customer.', max_length=2, null=True, verbose_name='Country'),
        ),
    ]