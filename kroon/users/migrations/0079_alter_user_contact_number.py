# Generated by Django 3.2.9 on 2022-04-23 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0078_auto_20220420_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact_number',
            field=models.CharField(help_text='The contact number of the customer.', max_length=25, null=True, unique=True, verbose_name='Contact number'),
        ),
    ]
