# Generated by Django 3.2.9 on 2022-01-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0029_auto_20220123_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='message',
            field=models.CharField(help_text='Transactions message that was taken by the customer.', max_length=300, null=True, verbose_name='Transaction Message'),
        ),
    ]