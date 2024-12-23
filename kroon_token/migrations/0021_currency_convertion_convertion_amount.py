# Generated by Django 3.2.9 on 2023-02-15 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroon_token', '0020_currency_convertion'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency_convertion',
            name='convertion_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=1.0, help_text='this holds the convertion amount for each country.', max_digits=300, null=True, verbose_name='Convertion Amount'),
        ),
    ]
