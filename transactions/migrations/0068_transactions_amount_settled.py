# Generated by Django 3.2.9 on 2022-03-25 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0067_auto_20220324_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='amount_settled',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='the final amount settled by the third providers , note this takes place when they have reducted their trasaction charges.', max_digits=300, null=True, verbose_name='Amount Settled'),
        ),
    ]
