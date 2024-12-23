# Generated by Django 3.2.9 on 2022-02-03 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0051_user_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ManyToManyField(blank=True, help_text='The users address which can be business address or home address,', related_name='address', to='users.UserAddress', verbose_name='User Address'),
        ),
    ]
