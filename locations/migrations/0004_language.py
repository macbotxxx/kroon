# Generated by Django 3.2.9 on 2022-06-12 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_alter_country_accept_kroon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(blank=True, help_text='this represents the language name', max_length=255, null=True, verbose_name='Language name')),
                ('language_ISO2', models.CharField(blank=True, help_text='the language iso 2 ', max_length=2, null=True, verbose_name='Language ISO 2 code')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Language',
                'db_table': 'countries_language',
            },
        ),
    ]
