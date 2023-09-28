# Generated by Django 3.2.9 on 2022-10-05 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_cards', '0007_delete_create_virtual_cards'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtual_cards_details',
            name='block',
            field=models.BooleanField(blank=True, default=False, help_text=' This indicates if the card is block or not ', null=True, verbose_name='Card Block'),
        ),
    ]
