# Generated by Django 3.2.9 on 2022-08-06 22:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workers_Logs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('login_time', models.DateTimeField(blank=True, help_text='The time at which the account will be logged in.', null=True, verbose_name='Login Time Record')),
                ('logout_time', models.DateTimeField(blank=True, help_text='The time at which the account will be logged out.', null=True, verbose_name='Logout Time Record')),
                ('merchant_account', models.ForeignKey(help_text='The user for whom the business belongs to , in other words the merchant profile', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_account', to=settings.AUTH_USER_MODEL, verbose_name='Merchant Profile')),
                ('worker_account', models.ForeignKey(help_text='this have the worker profile associated with the current merchant profile', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='worker_account', to=settings.AUTH_USER_MODEL, verbose_name='Worker Profile')),
            ],
            options={
                'verbose_name': 'Workers Logs',
                'verbose_name_plural': 'Workers Logs',
                'ordering': ('-created_date',),
            },
        ),
    ]