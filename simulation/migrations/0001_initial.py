# Generated by Django 3.2.9 on 2023-05-15 22:39

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Simulate_Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('country_iso2', models.CharField(help_text='this stores the country iso2 value for identification for the onboarding process', max_length=2, null=True, verbose_name='Country ISO2')),
                ('number_of_merchants', models.IntegerField(help_text='this holds the number of merchants that will be onboarded for that particular country using the above iso2 value for identification for the onboarding process.', null=True, verbose_name='Number of Merchants')),
                ('submitted', models.BooleanField(default=False, help_text='this indicates whether the action is submitted successfully', null=True, verbose_name='submitted')),
                ('processing_status', models.BooleanField(default=False, help_text='this indicates whether the action is submitted successfully', null=True, verbose_name='processing status')),
            ],
            options={
                'verbose_name': 'simulated merchants',
                'verbose_name_plural': 'simulated merchants',
                'ordering': ('-created_date',),
            },
        ),
    ]
