# Generated by Django 3.2.9 on 2021-12-13 01:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='English name of country', max_length=255, verbose_name='Country Name')),
                ('phone_code', models.CharField(blank=True, help_text='Countries International dialing phone code.', max_length=100, null=True, verbose_name='Phone Code')),
                ('currency', models.CharField(blank=True, help_text='Official country currency.', max_length=50, null=True, verbose_name='Currency')),
                ('iso2', models.CharField(blank=True, help_text='Two-letter country code', max_length=2, null=True, verbose_name='ISO2')),
                ('native', models.CharField(blank=True, help_text='Localized or native language of country.', max_length=255, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Timestamp when the record was created', verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Timestamp when the record was modified.', verbose_name='Modified Date')),
                ('accept_signup', models.BooleanField(default=True, help_text='Allow users from country to register.', verbose_name='Accept Registration')),
                ('banned', models.BooleanField(default=False, help_text='Indicate if country is banned or not', verbose_name='Banned')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'db_table': 'countries',
            },
        ),
    ]