# Generated by Django 3.2.9 on 2022-03-15 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0061_auto_20220302_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='credited_kroon_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='created amount taken by the customer.', max_digits=300, null=True, verbose_name='Credited Amount'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='debited_kroon_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='debited amount taken by the customer.', max_digits=300, null=True, verbose_name='Debited Amount'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='kroon_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='the remaining kroon balance amount taken for the customer.', max_digits=300, null=True, verbose_name='Kroon Balance'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='currency',
            field=models.CharField(help_text='Transactional currency message that was taken by the customer.', max_length=300, null=True, verbose_name='Kroon Currency'),
        ),
    ]
