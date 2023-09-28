# Generated by Django 3.2.9 on 2022-03-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0056_transactions_local_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kroontokenrequest',
            name='amount_in_kroon_token',
            field=models.FloatField(help_text='transactional amount taken by the customer.', null=True, verbose_name='Amount In Kroon Token'),
        ),
        migrations.AlterField(
            model_name='kroontokentransfer',
            name='kroon_token',
            field=models.FloatField(help_text='transactional amount taken by the customer.', null=True, verbose_name='Amount In Kroon Token'),
        ),
        migrations.AlterField(
            model_name='userrequesttoken',
            name='amount_in_kroon_token',
            field=models.FloatField(blank=True, help_text='transactional amount taken by the customer.', null=True, verbose_name='Amount In Kroon Token'),
        ),
    ]
