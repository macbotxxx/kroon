# Generated by Django 3.2.9 on 2022-04-23 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0079_alter_user_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact_number',
            field=models.CharField(help_text='The contact number of the customer.', max_length=13, null=True, unique=True, verbose_name='Contact number'),
        ),
    ]