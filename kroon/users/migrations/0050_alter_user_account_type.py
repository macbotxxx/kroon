# Generated by Django 3.2.9 on 2022-01-31 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0049_auto_20220129_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(blank=True, choices=[('personal', 'Personal'), ('merchant', 'Merchant')], default='borrower', help_text='Account type', max_length=15, null=True, verbose_name='Account Type'),
        ),
    ]
