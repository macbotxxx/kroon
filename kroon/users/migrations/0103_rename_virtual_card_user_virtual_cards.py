# Generated by Django 3.2.9 on 2022-10-06 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0102_user_virtual_card'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='virtual_card',
            new_name='virtual_cards',
        ),
    ]