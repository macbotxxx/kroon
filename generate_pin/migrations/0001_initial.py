# Generated by Django 3.2.9 on 2022-03-26 16:47

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
            name='Generate_Pin',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('pin', models.IntegerField(help_text='this is the generated pin for the user to enable the user to recieve token request offers which is a one time pin.', null=True, verbose_name='Pin')),
                ('user', models.ForeignKey(help_text='The user that is currently sending kroon token.', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Generator Profile')),
            ],
            options={
                'verbose_name': 'Generated Pin',
                'verbose_name_plural': 'Generated Pin',
                'ordering': ('-created_date',),
            },
        ),
    ]
