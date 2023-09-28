# Generated by Django 3.2.9 on 2021-12-14 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0002_auto_20211214_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='KroonTokenTransfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('kroon_token', models.PositiveIntegerField(help_text='transactional amount taken by the customer.', null=True, verbose_name='Amount In Kroon Token')),
                ('status', models.BooleanField(default=False, help_text='transactional status which determines whether the transaction was successful or not .', null=True, verbose_name='Transaction Status')),
                ('reciever', models.ForeignKey(help_text='The user for whom account belongs to', on_delete=django.db.models.deletion.PROTECT, related_name='reciever', to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
                ('sender', models.ForeignKey(help_text='The user that is currently sending kroon token.', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
                ('transactional_id', models.ForeignKey(editable=False, help_text='Transaction identifier that belongs to the customer', null=True, on_delete=django.db.models.deletion.PROTECT, to='transactions.transactions', verbose_name='Transactional ID')),
            ],
            options={
                'verbose_name': 'All Kroon Token Transfer',
                'verbose_name_plural': 'All Kroon Token Transfer',
                'ordering': ('created_date',),
            },
        ),
    ]
