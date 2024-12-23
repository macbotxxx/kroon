# Generated by Django 3.2.9 on 2022-10-04 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroon_kyc', '0015_kycapplication_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='marchantkycapplication',
            name='state',
            field=models.CharField(help_text='The state of the user submitting KYC application. Must be from the users country of Residence indicated at the time of registration.', max_length=255, null=True, verbose_name='State'),
        ),
    ]
