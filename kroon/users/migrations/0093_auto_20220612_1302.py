# Generated by Django 3.2.9 on 2022-06-12 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0092_alter_businessprofile_business_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessprofile',
            name='web_dark_mode',
            field=models.BooleanField(default=False, help_text='the active status bar indicates if the merchant business is on dark mode or not ', null=True, verbose_name='Web Dark Mode'),
        ),
        migrations.AddField(
            model_name='businessprofile',
            name='web_light_mode',
            field=models.BooleanField(default=True, help_text='the active status bar indicates if the merchant business is on light mode or not ', null=True, verbose_name='Web Light Mode'),
        ),
    ]
