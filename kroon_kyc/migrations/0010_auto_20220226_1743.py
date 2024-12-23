# Generated by Django 3.2.9 on 2022-02-26 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0001_initial'),
        ('kroon_kyc', '0009_remove_marchantkycapplication_registered_ip_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marchantkycapplication',
            old_name='company_registration_number',
            new_name='identification_number',
        ),
        migrations.RemoveField(
            model_name='marchantkycapplication',
            name='status_update_date',
        ),
        migrations.AddField(
            model_name='marchantkycapplication',
            name='birth_date',
            field=models.DateField(blank=True, help_text="The user's date of birth as per the identification document. The date of birth must match The user's ID", null=True, verbose_name='Date of Birth'),
        ),
        migrations.AddField(
            model_name='marchantkycapplication',
            name='business_registration_number',
            field=models.CharField(blank=True, help_text='the business registration number of the user submitting KYC application', max_length=255, null=True, verbose_name='Business Name Registration Number'),
        ),
        migrations.AddField(
            model_name='marchantkycapplication',
            name='email',
            field=models.EmailField(blank=True, help_text='The primary e-mail address of the user submitting KYC application', max_length=150, verbose_name='Email Address'),
        ),
        migrations.AddField(
            model_name='marchantkycapplication',
            name='identification_expiry',
            field=models.DateField(blank=True, help_text='The date of expiry of the identification document provided by the user', null=True, verbose_name='ID Expiry date'),
        ),
        migrations.AddField(
            model_name='marchantkycapplication',
            name='identification_issue_date',
            field=models.DateField(blank=True, help_text='The date of issue of the identification document provided by the user', null=True, verbose_name='ID Issue date'),
        ),
        migrations.AddField(
            model_name='marchantkycapplication',
            name='legal_first_names',
            field=models.CharField(blank=True, help_text='First name of the user submitting KYC application - As shown in documents.', max_length=255, null=True, verbose_name='Legal First names'),
        ),
        migrations.AddField(
            model_name='marchantkycapplication',
            name='legal_last_names',
            field=models.CharField(blank=True, help_text='First name of the user submitting KYC application - As shown in documents.', max_length=255, null=True, verbose_name='Legal Last names'),
        ),
        migrations.AlterField(
            model_name='marchantkycapplication',
            name='kyc_country',
            field=models.ForeignKey(blank=True, help_text='Country for which KYC has been performed against user. Each country may have different set of fields for KYC. This flag drives the system to show or hide the necessary fields.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='merchant_country', to='locations.country', verbose_name='KYC Country'),
        ),
        migrations.AlterField(
            model_name='marchantkycapplication',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Unique identifier of the user that owns the activity.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='KYC User'),
        ),
    ]
