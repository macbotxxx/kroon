# Generated by Django 3.2.9 on 2022-05-15 12:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0080_alter_user_contact_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessprofile',
            name='workers',
            field=models.ManyToManyField(help_text='this field holds the company workers profile account which will automatically be associated with the user profile account.', related_name='worker_profile', to=settings.AUTH_USER_MODEL, verbose_name='Worker Profile'),
        ),
    ]
