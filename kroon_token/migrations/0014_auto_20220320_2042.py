# Generated by Django 3.2.9 on 2022-03-20 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroon_token', '0013_auto_20220302_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasetokenfees',
            name='application_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='identify the application fees for the current rate.', max_digits=300, max_length=3, null=True, verbose_name='Application Fees'),
        ),
        migrations.AlterField(
            model_name='purchasetokenfees',
            name='vat_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='the vat fee for any transaction which will be calculated with the kroon token amount and application fees.', max_digits=300, max_length=3, null=True, verbose_name='Vat Fees'),
        ),
        migrations.AlterField(
            model_name='withdrawtokenfees',
            name='application_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='identify the application fees for the current rate, this is also known as the CASHOUT FEES.', max_digits=300, max_length=4, null=True, verbose_name='Application Fees'),
        ),
        migrations.AlterField(
            model_name='withdrawtokenfees',
            name='vat_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='the vat fee for any transaction which will be calculated with the kroon token amount and application fees.', max_digits=300, max_length=4, null=True, verbose_name='Vat Fees'),
        ),
    ]
