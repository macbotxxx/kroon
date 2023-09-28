from datetime import date, datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
 
from kroon.users.models import User
 
 
from helpers.common.basemodel import BaseModel
from helpers.common.choices import ModelChoices
from locations.models import Country



class KYC_Document(BaseModel):
    """
    A KYC or Know Your Customer is used to gather information on user in a regular interval.
    The KYCs collect information such as where they live, collecting their updated or different ID
    information, and their risk level at that point in time.
 
    Know Your Client (KYC) is a requirement that protects both financial institutions and their users. Financial institutions are required to formally verify the identity of all users and understand the purpose of trading, expected volumes and jurisdictions their users will use.
 
    Identity verification is a requirement for companies across a range of industries. Veriff offers compliance, fraud prevention and global scalability.
    """

    # region Fields
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('KYC User'), null=True, blank=True,
        help_text=_('Unique identifier of the user that owns the activity.'))

    wallet_id = models.CharField(
        max_length=255,
        verbose_name=_('Legal First names'),
        blank=True, null=True,
        help_text=_("First name of the user submitting KYC application - As shown in documents."))
 
#     legal_last_names = models.CharField(
#         max_length=255,
#         verbose_name=_('Legal Last names'),
#         blank=True, null=True,
#         help_text=_("Last name of the user submitting KYC application - As shown in documents."))
 
#     birth_date = models.DateField(
#         verbose_name=_('Date of Birth'),
#         blank=True, null=True,
#         help_text=_("""The user's date of birth as per the identification document. The date of birth must match The user's ID"""))
 
#     email = models.EmailField(
#         verbose_name=_('Email Address'),
#         max_length=150,
#         blank=True,
#         help_text=_("The primary e-mail address of the user submitting KYC application"))
 
#     street_or_flat_number = models.CharField(
#         verbose_name=_("Street or Flat Number"),
#         null=True, blank=True,
#         max_length=50,
#         help_text='Street or Flat Number"), of the user')

#     street_name = models.CharField(
#         verbose_name=_("Street Name"),
#         null=True, blank=True,
#         max_length=50,
#         help_text='Street Name of the user')

#     building_name = models.CharField(
#         verbose_name=_("Building Name"),
#         null=True, blank=True,
#         max_length=50,
#         help_text='Building Name of the user')
 
#     zip_code = models.CharField(
#         max_length=10,
#         verbose_name=_('Zip Code'),
#         help_text=_("""The zip code or postal code of the user submitting KYC application. Must be from The user's country of Residence indicated at the time of registration."""))
 
#     city = models.CharField(
#         max_length=255,
#         verbose_name=_('City'),
#         help_text=_("""The city of the user submitting KYC application. Must be from the users country of Residence indicated at the time of registration."""))

#     state = models.CharField(
#         max_length=255,
#         null = True,
#         verbose_name=_('State'),
#         help_text=_("""The state of the user submitting KYC application. Must be from the users country of Residence indicated at the time of registration."""))
 
#     identification_type = models.CharField(
#         max_length=21,
#         choices=ModelChoices.PHOTO_IDENTIFICATION_TYPE,
#         default='national_id',
#         verbose_name=_('Photo ID Type'),
#         help_text=_("""The type of identification document that the user has provided to the bank such as passport or national ID card. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution."""))
 
#     photo_id = models.ImageField(
#         upload_to="uploads/kyc/",
#         verbose_name=_('Photo ID(front)'),
#         help_text=_("""The front side of The user's Photo Identitification. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution."""))
 
#     photo_id_back = models.ImageField(
#         upload_to="uploads/kyc/",
#         verbose_name=_('Photo ID(back)'),
#         blank=True, null=True,
#         help_text=_("""The back side of The user's Photo Identitification. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution."""))
 
#     selfie_with_id = models.ImageField(
#         upload_to="uploads/kyc/",
#         verbose_name=_('Selfie with ID'),
#         help_text=_(
#             """Upload a photo with yourself and your Passport or both sides of the ID Card. The face and the document must be clearly visible."""),
#         blank=True, null=True)
 
#     kyc_status = models.CharField(
#         max_length=28,
#         choices=ModelChoices.KYC_STATUS,
#         default='Pending',
#         verbose_name=_('KYC Status'),
#         help_text=_("The KYC status of the user. The default is `Unverified`."))
 
#     # status_update_date = models.DateTimeField(
#     #     default=timezone.now,
#     #     editable=False,
#     #     verbose_name=_('Status Update Time'),
#     #     help_text=_('Timestamp at which the resource status was updated.'))
 
#     identification_number = models.CharField(
#         max_length=50,
#         help_text=_(
#             "The number of the identification document provided by the person such as the passport number or the national ID card number."),
#         blank=True, null=True,
#         verbose_name=_('Photo Identification number'))

#     identification_issue_date = models.DateField(
#         blank=True, null=True,
#         help_text=_("""The date of issue of the identification document provided by the user"""),
#         verbose_name=_('ID Issue date'))
 
#     identification_expiry = models.DateField(
#         blank=True, null=True,
#         help_text=_("""The date of expiry of the identification document provided by the user"""),
#         verbose_name=_('ID Expiry date'))

#     kyc_country = models.ForeignKey(
#         Country,
#         on_delete=models.CASCADE,
#         blank=True, null=True,
#         verbose_name=_('KYC Country'),
#         help_text=_("""Country for which KYC has been performed against user. Each country may have different set of fields for KYC. This flag drives the system to show or hide the necessary fields."""),
#         related_name='kyc_country')

#     kyc_review_date = models.DateTimeField(
#         blank=True, null=True,
#         editable=False,
#         verbose_name=_('KYC Checked Date'),
#         help_text=_("""Date on which KYC check was performed."""))

#     accept_terms = models.BooleanField(
#         default=False,
#         verbose_name=_('Accepted Terms'),
#         help_text=_("""Agreements collected from the user, such as acceptance of terms and conditions, or opt in for marketing. This defaults to False."""))
 
#     agreed_to_data_usage = models.BooleanField(
#         default=False,
#         verbose_name=_('Agreed to Data Usage'),
#         help_text=_("""Consent to us using the provided data, including consent for us to verify the identity of relevant individuals with our service providers and database owners in accordance with the Identity Verification Terms. This defaults to False."""))
    
#     kyc_refused_code = models.CharField(
#         verbose_name=_("KYC Refused Code"),
#         max_length=34,
#         choices=ModelChoices.KYC_REFUSE_REASON_CODE,
#         blank=True, null=True,
#         help_text=_("The type of reason for refusal")
#     )
 
  
 
#     # region Metadata
#     class Meta:
#         verbose_name = _('KYC Application')
#         verbose_name_plural = _('KYC Applications')
#         db_table = 'kyc_applications'
#         permissions = [
#             ("verify_kyc", _("Verify KYC Application")),
#             ("reject_kyc", _("Reject KYC Application")),
#             ("merge_kyc", _("Merge KYC data with user Information")),
#         ]
#     # endregion
 
#     # region Methods
#     def __str__(self):
#         return str(self.user)
 
#     @property
#     def age(self):
#         return int((datetime.now().date() - self.birth_date).days / 365.25)
 
#     def get_user(self):
#         return str(self.user.pk)
 
#     get_object_user = property(get_user)
 
    # def clean_fields(self, exclude=None):
    #     super().clean_fields(exclude=exclude)
    #     if self.identification_issue_date == self.identification_expiry:
    #         raise ValidationError(
    #             {
    #                 'identification_issue_date': _(
    #                     "ID issue date and Expiry date cannot be the same."
    #                 ),
    #             }
    #         )
    #     if self.identification_issue_date > date.today():
    #         raise ValidationError({
    #             'identification_issue_date': _(
    #                 "We cannot time-travel into the future at the moment."
    #             ),
    #         }
    #         )
    #     if self.identification_expiry == date.today() or self.identification_expiry < date.today():
    #         raise ValidationError({
    #             'identification_expiry': _(
    #                 "We cannot travel back in time. ID has expired."
    #             ),
    #         }
    #         )
 
    # endregion
 




 
class KycApplication(BaseModel):

    """
    A KYC or Know Your Customer is used to gather information on user in a regular interval.
    The KYCs collect information such as where they live, collecting their updated or different ID
    information, and their risk level at that point in time.
 
    Know Your Client (KYC) is a requirement that protects both financial institutions and their users. Financial institutions are required to formally verify the identity of all users and understand the purpose of trading, expected volumes and jurisdictions their users will use.
 
    Identity verification is a requirement for companies across a range of industries. Veriff offers compliance, fraud prevention and global scalability.
    """
    # region Fields
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('KYC User'), null=True, blank=True,
        help_text=_('Unique identifier of the user that owns the activity.'))

    legal_first_names = models.CharField(
        max_length=255,
        verbose_name=_('Legal First names'),
        blank=True, null=True,
        help_text=_("First name of the user submitting KYC application - As shown in documents."))
 
    legal_last_names = models.CharField(
        max_length=255,
        verbose_name=_('Legal Last names'),
        blank=True, null=True,
        help_text=_("Last name of the user submitting KYC application - As shown in documents."))
 
    birth_date = models.DateField(
        verbose_name=_('Date of Birth'),
        blank=True, null=True,
        help_text=_("""The user's date of birth as per the identification document. The date of birth must match The user's ID"""))
 
    email = models.EmailField(
        verbose_name=_('Email Address'),
        max_length=150,
        blank=True,
        help_text=_("The primary e-mail address of the user submitting KYC application"))
 
    street_or_flat_number = models.CharField(
        verbose_name=_("Street or Flat Number"),
        null=True, blank=True,
        max_length=50,
        help_text='Street or Flat Number"), of the user')

    street_name = models.CharField(
        verbose_name=_("Street Name"),
        null=True, blank=True,
        max_length=50,
        help_text='Street Name of the user')

    building_name = models.CharField(
        verbose_name=_("Building Name"),
        null=True, blank=True,
        max_length=50,
        help_text='Building Name of the user')
 
    zip_code = models.CharField(
        max_length=10,
        verbose_name=_('Zip Code'),
        help_text=_("""The zip code or postal code of the user submitting KYC application. Must be from The user's country of Residence indicated at the time of registration."""))
 
    city = models.CharField(
        max_length=255,
        verbose_name=_('City'),
        help_text=_("""The city of the user submitting KYC application. Must be from the users country of Residence indicated at the time of registration."""))

    state = models.CharField(
        max_length=255,
        null = True,
        verbose_name=_('State'),
        help_text=_("""The state of the user submitting KYC application. Must be from the users country of Residence indicated at the time of registration."""))
 
    identification_type = models.CharField(
        max_length=21,
        choices=ModelChoices.PHOTO_IDENTIFICATION_TYPE,
        default='national_id',
        verbose_name=_('Photo ID Type'),
        help_text=_("""The type of identification document that the user has provided to the bank such as passport or national ID card. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution."""))
 
    photo_id = models.ImageField(
        upload_to="uploads/kyc/",
        verbose_name=_('Photo ID(front)'),
        help_text=_("""The front side of The user's Photo Identitification. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution."""))
 
    photo_id_back = models.ImageField(
        upload_to="uploads/kyc/",
        verbose_name=_('Photo ID(back)'),
        blank=True, null=True,
        help_text=_("""The back side of The user's Photo Identitification. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution."""))
 
    selfie_with_id = models.ImageField(
        upload_to="uploads/kyc/",
        verbose_name=_('Selfie with ID'),
        help_text=_(
            """Upload a photo with yourself and your Passport or both sides of the ID Card. The face and the document must be clearly visible."""),
        blank=True, null=True)
 
    kyc_status = models.CharField(
        max_length=28,
        choices=ModelChoices.KYC_STATUS,
        default='Pending',
        verbose_name=_('KYC Status'),
        help_text=_("The KYC status of the user. The default is `Unverified`."))
 
    # status_update_date = models.DateTimeField(
    #     default=timezone.now,
    #     editable=False,
    #     verbose_name=_('Status Update Time'),
    #     help_text=_('Timestamp at which the resource status was updated.'))
 
    identification_number = models.CharField(
        max_length=50,
        help_text=_(
            "The number of the identification document provided by the person such as the passport number or the national ID card number."),
        blank=True, null=True,
        verbose_name=_('Photo Identification number'))

    identification_issue_date = models.DateField(
        blank=True, null=True,
        help_text=_("""The date of issue of the identification document provided by the user"""),
        verbose_name=_('ID Issue date'))
 
    identification_expiry = models.DateField(
        blank=True, null=True,
        help_text=_("""The date of expiry of the identification document provided by the user"""),
        verbose_name=_('ID Expiry date'))

    kyc_country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name=_('KYC Country'),
        help_text=_("""Country for which KYC has been performed against user. Each country may have different set of fields for KYC. This flag drives the system to show or hide the necessary fields."""),
        related_name='kyc_country')

    kyc_review_date = models.DateTimeField(
        blank=True, null=True,
        editable=False,
        verbose_name=_('KYC Checked Date'),
        help_text=_("""Date on which KYC check was performed."""))

    accept_terms = models.BooleanField(
        default=False,
        verbose_name=_('Accepted Terms'),
        help_text=_("""Agreements collected from the user, such as acceptance of terms and conditions, or opt in for marketing. This defaults to False."""))
 
    agreed_to_data_usage = models.BooleanField(
        default=False,
        verbose_name=_('Agreed to Data Usage'),
        help_text=_("""Consent to us using the provided data, including consent for us to verify the identity of relevant individuals with our service providers and database owners in accordance with the Identity Verification Terms. This defaults to False."""))
    
    kyc_refused_code = models.CharField(
        verbose_name=_("KYC Refused Code"),
        max_length=34,
        choices=ModelChoices.KYC_REFUSE_REASON_CODE,
        blank=True, null=True,
        help_text=_("The type of reason for refusal")
    )
 
  
 
    # region Metadata
    class Meta:
        verbose_name = _('KYC Application')
        verbose_name_plural = _('KYC Applications')
        db_table = 'kyc_applications'
        permissions = [
            ("verify_kyc", _("Verify KYC Application")),
            ("reject_kyc", _("Reject KYC Application")),
            ("merge_kyc", _("Merge KYC data with user Information")),
        ]
    # endregion
 
    # region Methods
    def __str__(self):
        return str(self.user)
 
    @property
    def age(self):
        return int((datetime.now().date() - self.birth_date).days / 365.25)
 
    def get_user(self):
        return str(self.user.pk)
 
    get_object_user = property(get_user)
 
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.identification_issue_date == self.identification_expiry:
            raise ValidationError(
                {
                    'identification_issue_date': _(
                        "ID issue date and Expiry date cannot be the same."
                    ),
                }
            )
        if self.identification_issue_date > date.today():
            raise ValidationError({
                'identification_issue_date': _(
                    "We cannot time-travel into the future at the moment."
                ),
            }
            )
        if self.identification_expiry == date.today() or self.identification_expiry < date.today():
            raise ValidationError({
                'identification_expiry': _(
                    "We cannot travel back in time. ID has expired."
                ),
            }
            )
 
    # endregion
 
 
 

 
class MarchantKycApplication(BaseModel):
    """
    A KYC or Know Your Customer is used to gather information on user in a regular interval.
    The KYCs collect information such as where they live, collecting their updated or different ID
    information, and their risk level at that point in time.
 
    Know Your Client (KYC) is a requirement that protects both financial institutions and their users. Financial institutions are required to formally verify the identity of all users and understand the purpose of trading, expected volumes and jurisdictions their users will use.
 
    Identity verification is a requirement for companies across a range of industries. Veriff offers compliance, fraud prevention and global scalability.
    """
    # region Fields
    # region Fields
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('KYC User'), null=True, 
        help_text=_('Unique identifier of the user that owns the activity.'))

    legal_first_names = models.CharField(
        max_length=255,
        verbose_name=_('Legal First names'),
         null=True,
        help_text=_("First name of the user submitting KYC application - As shown in documents."))
 
    legal_last_names = models.CharField(
        max_length=255,
        verbose_name=_('Legal Last names'),
         null=True,
        help_text=_("First name of the user submitting KYC application - As shown in documents."))
 
    birth_date = models.DateField(
        verbose_name=_('Date of Birth'),
         null=True,
        help_text=_("""The user's date of birth as per the identification document. The date of birth must match The user's ID"""))
 
    email = models.EmailField(
        verbose_name=_('Email Address'),
        max_length=150,
        
        help_text=_("The primary e-mail address of the user submitting KYC application"))
 
    street_or_flat_number = models.CharField(
        verbose_name=_("Street or Flat Number"),
        null=True, blank=True,
        max_length=50,
        help_text='Street or Flat Number"), of the user')

    street_name = models.CharField(
        verbose_name=_("Street Name"),
        null=True, blank=True,
        max_length=50,
        help_text='Street Name of the user')

    building_name = models.CharField(
        verbose_name=_("Building Name"),
        null=True, blank=True,
        max_length=50,
        help_text='Building Name of the user')
 
    zip_code = models.CharField(
        max_length=10,
        verbose_name=_('Zip Code'),
        help_text=_("""The zip code or postal code of the user submitting KYC application. Must be from The user's country of Residence indicated at the time of registration."""))
 
    city = models.CharField(
        max_length=255,
        verbose_name=_('City'),
        help_text=_("""The city of the user submitting KYC application. Must be from the users country of Residence indicated at the time of registration."""))

    state = models.CharField(
        max_length=255,
        null = True,
        verbose_name=_('State'),
        help_text=_("""The state of the user submitting KYC application. Must be from the users country of Residence indicated at the time of registration."""))
 
    identification_type = models.CharField(
        max_length=21,
        choices=ModelChoices.PHOTO_IDENTIFICATION_TYPE,
        default='national_id',
        verbose_name=_('Photo ID Type'),
        help_text=_("""The type of identification document that the user has provided to the bank such as passport or national ID card. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution."""))
 
    photo_id = models.ImageField(
        upload_to="uploads/kyc/",
        verbose_name=_('Photo ID(front)'),
        help_text=_("""The front side of The user's Photo Identitification. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution."""))
 
    photo_id_back = models.ImageField(
        upload_to="uploads/kyc/",
        verbose_name=_('Photo ID(back)'),
        blank=True, null=True,
        help_text=_("""The back side of The user's Photo Identitification. Chosen credential must not be expired. Document should be good condition and clearly visible. File is at least 1 MB in size and has at least 300 dpi resolution."""))
 
    selfie_with_id = models.ImageField(
        upload_to="uploads/kyc/",
        verbose_name=_('Selfie with ID'),
        help_text=_(
            """Upload a photo with yourself and your Passport or both sides of the ID Card. The face and the document must be clearly visible."""),
        blank=True, null=True)
 
    kyc_status = models.CharField(
        max_length=28,
        choices=ModelChoices.KYC_STATUS,
        default='Pending',
        verbose_name=_('KYC Status'),
        help_text=_("The KYC status of the user. The default is `Unverified`."))
 
    # status_update_date = models.DateTimeField(
    #     default=timezone.now,
    #     editable=False,
    #     verbose_name=_('Status Update Time'),
    #     help_text=_('Timestamp at which the resource status was updated.'))
 
    identification_number = models.CharField(
        max_length=50,
        help_text=_(
            "The number of the identification document provided by the person such as the passport number or the national ID card number."),
        blank=True, null=True,
        verbose_name=_('Photo Identification number'))

    identification_issue_date = models.DateField(
        blank=True, null=True,
        help_text=_("""The date of issue of the identification document provided by the user"""),
        verbose_name=_('ID Issue date'))
 
    identification_expiry = models.DateField(
        blank=True, null=True,
        help_text=_("""The date of expiry of the identification document provided by the user"""),
        verbose_name=_('ID Expiry date'))

    kyc_country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
         null=True, 
        verbose_name=_('KYC Country'),
        help_text=_("""Country for which KYC has been performed against user. Each country may have different set of fields for KYC. This flag drives the system to show or hide the necessary fields."""),
        related_name='merchant_country')

    kyc_review_date = models.DateTimeField(
        blank=True, null=True,
        editable=False,
        verbose_name=_('KYC Checked Date'),
        help_text=_("""Date on which KYC check was performed."""))

    accept_terms = models.BooleanField(
        default=False,
        verbose_name=_('Accepted Terms'),
        help_text=_("""Agreements collected from the user, such as acceptance of terms and conditions, or opt in for marketing. This defaults to False."""))
 
    agreed_to_data_usage = models.BooleanField(
        default=False,
        verbose_name=_('Agreed to Data Usage'),
        help_text=_("""Consent to us using the provided data, including consent for us to verify the identity of relevant individuals with our service providers and database owners in accordance with the Identity Verification Terms. This defaults to False."""))
    
    kyc_refused_code = models.CharField(
        verbose_name=_("KYC Refused Code"),
        max_length=34,
        choices=ModelChoices.KYC_REFUSE_REASON_CODE,
        blank=True, null=True,
        help_text=_("The type of reason for refusal")
    )

    legal_business_name = models.CharField(
        max_length=255,
        verbose_name=_('Business Name'),
         null=True,
        help_text=_("the business name of the user submitting KYC application"))
 
    business_email = models.EmailField(
        verbose_name=_('Email Address'),
        max_length=150,
        null=True,
        help_text=_("The primary e-mail address of the user business submitting KYC application"))

    business_registration_number = models.CharField(
        max_length=255,
        verbose_name=_('Business Name Registration Number'),
         null=True,
        help_text=_("the business registration number of the user submitting KYC application"))
 
   
  
 
    # region Metadata
    class Meta:
        verbose_name = _('Marchant KYC Application')
        verbose_name_plural = _('Marchant KYC Applications')
        db_table = 'marchant_kyc_applications'
        permissions = [
            ("verify_kyc", _("Verify KYC Application")),
            ("reject_kyc", _("Reject KYC Application")),
            ("merge_kyc", _("Merge KYC data with user Information")),
        ]
    # endregion
 
    # region Methods
    def __str__(self):
        return str(self.user)
 
    # @property
    # def age(self):
    #     return int((datetime.now().date() - self.birth_date).days / 365.25)
 
    def get_user(self):
        return str(self.user.pk)
 
    get_object_user = property(get_user)
 
    # def clean_fields(self, exclude=None):
    #     super().clean_fields(exclude=exclude)
    #     if self.identification_issue_date == self.identification_expiry:
    #         raise ValidationError(
    #             {
    #                 'identification_issue_date': _(
    #                     "ID issue date and Expiry date cannot be the same."
    #                 ),
    #             }
    #         )
    #     if self.identification_issue_date > date.today():
    #         raise ValidationError({
    #             'identification_issue_date': _(
    #                 "We cannot time-travel into the future at the moment."
    #             ),
    #         }
    #         )
    #     if self.identification_expiry == date.today() or self.identification_expiry < date.today():
    #         raise ValidationError({
    #             'identification_expiry': _(
    #                 "We cannot travel back in time. ID has expired."
    #             ),
    #         }
    #         )
 
    # endregion
 
 
 