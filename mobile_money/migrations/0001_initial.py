# Generated by Django 3.2.9 on 2022-01-25 22:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkProvider',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('network_provider', models.CharField(help_text='this input receives network provider allowed in the users country.', max_length=70, null=True, verbose_name='Network Provider')),
                ('active', models.BooleanField(default=False, help_text='this indicates whether the network provider is active or not', null=True, verbose_name='Active')),
                ('country', models.ForeignKey(help_text='country that this network provider is allowed in', null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.country')),
            ],
            options={
                'verbose_name': 'Mobile Money Network Provider',
                'verbose_name_plural': 'Mobile Money Network Provider',
                'ordering': ('-created_date',),
            },
        ),
    ]