# Generated by Django 3.2.9 on 2021-12-14 00:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='amount',
        ),
        migrations.AddField(
            model_name='transactions',
            name='action',
            field=models.CharField(help_text='Transactions actions that was taken by the customer.', max_length=300, null=True, verbose_name='Transaction Action'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='amount_in_kroon_token',
            field=models.PositiveIntegerField(help_text='transactional amount taken by the customer.', null=True, verbose_name='Amount In Kroon Token'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='amount_in_user_default_currency',
            field=models.PositiveIntegerField(help_text='transactional amount taken by the customer.', null=True, verbose_name='Amount In User Default Currency'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='transactional_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Transaction identifier that belongs to the customer', null=True, unique=True, verbose_name='Transactional ID'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='user_default_currency',
            field=models.CharField(help_text='Default currency for the customer which the transaction belongs to.', max_length=5, null=True, verbose_name='Default Currency ID'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('cancelled', 'Cancelled'), ('rejected', 'Rejected/Refused')], default='pending', help_text='action status for the current transaction, which determines if it successful or not.', max_length=20, null=True, verbose_name='Transaction Status'),
        ),
    ]
