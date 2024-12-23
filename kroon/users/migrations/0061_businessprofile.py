# Generated by Django 3.2.9 on 2022-02-28 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0060_alter_user_device_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('business_id', models.CharField(help_text='business id is used as a special indicator to identify the user business.', max_length=255, null=True, verbose_name='Business ID')),
                ('business_logo', models.ImageField(blank=True, help_text='business logo for the merchant business account.', null=True, upload_to='images/business/logo', verbose_name='Business Logo')),
                ('business_name', models.CharField(help_text='the merchant user business name.', max_length=255, null=True, verbose_name='Business Name')),
                ('business_contact_number', models.CharField(help_text='the merchant user business contact number', max_length=255, null=True, verbose_name='Business Contact Number')),
                ('business_address', models.CharField(help_text='the merchant user business address', max_length=255, null=True, verbose_name='Business Address')),
                ('active', models.BooleanField(default=True, help_text='the active status bar indicates if the merchant business is active or not', null=True, verbose_name='Active')),
                ('user', models.ForeignKey(help_text='The user for whom account belongs to', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
            ],
            options={
                'verbose_name': 'Merchant Business Profile',
                'verbose_name_plural': 'Merchant Business Profile',
                'ordering': ('-created_date',),
            },
        ),
    ]
