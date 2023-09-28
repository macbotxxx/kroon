# Generated by Django 3.2.9 on 2021-12-13 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_user_country_of_residence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='available_balance',
        ),
        migrations.RemoveField(
            model_name='user',
            name='referral_bonus',
        ),
        migrations.AddField(
            model_name='user',
            name='kroon_token',
            field=models.FloatField(blank=True, default=0, help_text='The customers available kroon token for the account', null=True, verbose_name='Available Kroon Token'),
        ),
    ]
