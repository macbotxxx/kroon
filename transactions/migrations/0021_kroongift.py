# Generated by Django 3.2.9 on 2021-12-24 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0020_payment_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='KroonGift',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('receiver', models.EmailField(help_text='receiver email that will received the gift kroon token.', max_length=254, null=True, verbose_name='Receiver Email')),
                ('transactional_id', models.CharField(editable=False, help_text='Transaction identifier that belongs to the customer', max_length=30, null=True, verbose_name='Transactional ID')),
                ('amount_in_kroon_token', models.PositiveIntegerField(help_text='transactional amount taken by the customer.', null=True, verbose_name='Amount In Kroon Token')),
                ('kroon_token_qrcode', models.ImageField(blank=True, help_text='Token qrcode is been generated from the customer token request.', null=True, upload_to='gift_token_barcode/', verbose_name='Kroon Token QR Code')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('cancelled', 'Cancelled'), ('rejected', 'Rejected/Refused'), ('received', 'Received')], default='pending', help_text='action status for the current transaction, which determines if it successful or not.', max_length=20, null=True, verbose_name='Transaction Status')),
                ('user', models.ForeignKey(help_text='The user for whom account belongs to', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
            ],
            options={
                'verbose_name': 'Token Gift',
                'verbose_name_plural': 'Token Gift',
                'ordering': ('-created_date',),
            },
        ),
    ]