# Generated by Django 3.2.9 on 2022-06-14 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0095_businessprofile_business_default_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessprofile',
            name='web_dark_mode',
        ),
    ]
