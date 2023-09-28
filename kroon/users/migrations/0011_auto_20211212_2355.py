# Generated by Django 3.2.9 on 2021-12-12 23:55

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_user_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.AddField(
            model_name='user',
            name='country_of_residence',
            field=django_countries.fields.CountryField(help_text='The resident country of the customer.', max_length=2, null=True, verbose_name='Country'),
        ),
    ]
