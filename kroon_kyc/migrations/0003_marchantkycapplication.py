# Generated by Django 3.2.9 on 2021-12-18 02:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0001_initial'),
        ('kroon_kyc', '0002_remove_kycapplication_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarchantKycApplication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('legal_business_name', models.CharField(blank=True, help_text='the business name of the user submitting KYC application', max_length=255, null=True, verbose_name='Business Name')),
                ('business_email', models.EmailField(blank=True, help_text='The primary e-mail address of the user business submitting KYC application', max_length=150, verbose_name='Email Address')),
                ('address_line_1', models.CharField(help_text="The Address Line 1 of the user submitting KYC application. Must be from The user's country of Residence indicated at the time of registration.", max_length=255, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(blank=True, help_text="The Address Line 2 of the user submitting KYC application. Must be from The user's country of Residence indicated at the time of registration.", max_length=255, null=True, verbose_name='Address Line 2')),
                ('zip_code', models.CharField(help_text="The zip code or postal code of the user submitting KYC application. Must be from The user's country of Residence indicated at the time of registration.", max_length=10, verbose_name='Zip Code')),
                ('city', models.CharField(help_text='The city of the user submitting KYC application. Must be from the users country of Residence indicated at the time of registration.', max_length=255, verbose_name='City')),
                ('identification_type', models.CharField(choices=[('national_id', 'National ID'), ('passport', 'Passport'), ('driver_license', 'Driver License')], default='national_id', help_text='The type of identification document that the user has provided to the bank such as passport or national ID card. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution.', max_length=21, verbose_name='Photo ID Type')),
                ('photo_id', models.FileField(help_text="The front side of The user's Photo Identitification. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution.", storage='uploads/kyc/', upload_to='', verbose_name='Photo ID(front)')),
                ('photo_id_back', models.FileField(blank=True, help_text="The back side of The user's Photo Identitification. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution.", null=True, storage='uploads/kyc/', upload_to='', verbose_name='Photo ID(back)')),
                ('selfie_with_id', models.FileField(blank=True, help_text='Upload a photo with yourself and your Passport or both sides of the ID Card. The face and the document must be clearly visible.', null=True, storage='uploads/kyc/', upload_to='', verbose_name='Selfie with ID')),
                ('kyc_status', models.CharField(choices=[('verified', 'Verified'), ('unverified', 'Unverified'), ('pending', 'Pending'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='Pending', help_text='The KYC status of the user. The default is `Unverified`.', max_length=28, verbose_name='KYC Status')),
                ('status_update_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Timestamp at which the resource status was updated.', verbose_name='Status Update Time')),
                ('company_registration_number', models.CharField(blank=True, help_text='The number of the identification document provided by the person such as the passport number or the national ID card number.', max_length=50, null=True, verbose_name='Photo Identification number')),
                ('kyc_submitted_ip_address', models.GenericIPAddressField(blank=True, editable=False, help_text='The IP address of the user recorded at the time of registration.', null=True, verbose_name='KYC Submitted IP')),
                ('kyc_review_date', models.DateTimeField(blank=True, editable=False, help_text='Date on which KYC check was performed.', null=True, verbose_name='KYC Checked Date')),
                ('registered_ip_address', models.GenericIPAddressField(blank=True, editable=False, help_text='The IP address of the user recorded at the time of registration. Registered IP address is compared with the Submitted IP address to make sure client is within the same region.', null=True, verbose_name='Registered IP')),
                ('accept_terms', models.BooleanField(default=False, help_text='Agreements collected from the user, such as acceptance of terms and conditions, or opt in for marketing. This defaults to False.', verbose_name='Accepted Terms')),
                ('agreed_to_data_usage', models.BooleanField(default=False, help_text='Consent to us using the provided data, including consent for us to verify the identity of relevant individuals with our service providers and database owners in accordance with the Identity Verification Terms. This defaults to False.', verbose_name='Agreed to Data Usage')),
                ('kyc_refused_code', models.CharField(blank=True, choices=[('EXPIRED_DOCUMENT', 'Document Expired'), ('INVALID_DOCUMENT', 'Invalid Document'), ('DOCUMENT_DOES_NOT_MATCH_USER_DATA', 'Document does not match user data.')], help_text='The type of reason for refusal', max_length=34, null=True, verbose_name='KYC Refused Code')),
                ('kyc_country', models.ForeignKey(blank=True, help_text='Country for which KYC has been performed against user. Each country may have different set of fields for KYC. This flag drives the system to show or hide the necessary fields.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='marchant_country', to='locations.country', verbose_name='KYC Country')),
                ('user', models.ForeignKey(help_text='Unique identifier of the user that owns the activity.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='KYC User')),
            ],
            options={
                'verbose_name': 'Marchant KYC Application',
                'verbose_name_plural': 'Marchant KYC Applications',
                'db_table': 'marchant_kyc_applications',
                'permissions': [('verify_kyc', 'Verify KYC Application'), ('reject_kyc', 'Reject KYC Application'), ('merge_kyc', 'Merge KYC data with user Information')],
            },
        ),
    ]