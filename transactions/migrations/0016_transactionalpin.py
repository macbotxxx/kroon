# Generated by Django 3.2.9 on 2021-12-16 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0015_auto_20211216_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionalPin',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('password', models.CharField(help_text='this input holds the user transaction pin which is been hased', max_length=500, null=True, verbose_name='Transactional Pin')),
                ('user', models.ForeignKey(help_text='The user for whom account belongs to', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
            ],
            options={
                'verbose_name': 'Users Transactional Pin',
                'verbose_name_plural': 'Users Transactional Pin',
                'ordering': ('-created_date',),
            },
        ),
    ]
