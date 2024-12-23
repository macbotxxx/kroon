# Generated by Django 3.2.9 on 2021-12-11 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_contact_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(blank=True, help_text='User kroon wallet id is unique to every user, the wallet id contains information about the customer', max_length=9, null=True, unique=True, verbose_name='Kroon Wallet ID'),
        ),
    ]
