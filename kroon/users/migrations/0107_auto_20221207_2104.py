# Generated by Django 3.2.9 on 2022-12-07 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0106_user_country_provence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='country_provence',
        ),
        migrations.AddField(
            model_name='user',
            name='country_province',
            field=models.CharField(blank=True, help_text='The users country province', max_length=40, null=True, verbose_name='Country Province'),
        ),
    ]
