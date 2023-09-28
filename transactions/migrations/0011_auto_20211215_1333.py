# Generated by Django 3.2.9 on 2021-12-15 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0010_auto_20211215_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kroontokenrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('cancelled', 'Cancelled'), ('rejected', 'Rejected/Refused'), ('received', 'Received')], default='pending', help_text='action status for the current transaction, which determines if it successful or not.', max_length=20, null=True, verbose_name='Transaction Status'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('cancelled', 'Cancelled'), ('rejected', 'Rejected/Refused'), ('received', 'Received')], default='pending', help_text='action status for the current transaction, which determines if it successful or not.', max_length=20, null=True, verbose_name='Transaction Status'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('payment_ref', models.CharField(help_text='The payment identification number sent from the payment gateway.', max_length=150, null=True, verbose_name='Payment Ref No')),
                ('payment_method', models.CharField(blank=True, default='Online Payment', help_text='The payment method used while paying for an order.', max_length=150, null=True, verbose_name='Payment Method')),
                ('amount_paid', models.IntegerField(help_text='Amount paid for the above order by the customer.', null=True, verbose_name='Amount Paid')),
                ('verified', models.BooleanField(blank=True, default=False, help_text='Verified payment status to identify if the payment is been verified by the payment gateway or not.', null=True, verbose_name='Payment Verification')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('cancelled', 'Cancelled'), ('rejected', 'Rejected/Refused'), ('received', 'Received')], default='pending', help_text='payment status to identify if the payment is been verified by the payment gateway or not.', max_length=150, null=True, verbose_name='Payment Status')),
                ('user', models.ForeignKey(help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
            ],
            options={
                'verbose_name': 'All Paystack Payment',
                'verbose_name_plural': 'All Paystack Payment',
                'ordering': ('-created_date',),
            },
        ),
    ]
