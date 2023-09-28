from django.utils.translation import gettext_lazy as _

class ModelChoices:

    PHOTO_IDENTIFICATION_TYPE = (
        ('national_id', _('National ID')),
        ('passport', _('Passport')),
        ('driver_license', _('Driver License')),
    )


    KYC_STATUS = (
        ('verified', _('Verified')),
        ('unverified', _('Unverified')),
        ('pending', _('Pending')),
        ('rejected', _('Rejected')),
        ('cancelled', _('Cancelled'))
    )

    KYC_REFUSE_REASON_CODE = (
        ('EXPIRED_DOCUMENT', _('Document Expired')),
        ('INVALID_DOCUMENT', _('Invalid Document')),
        ('DOCUMENT_DOES_NOT_MATCH_USER_DATA', _('Document does not match user data.'))
    )

    
