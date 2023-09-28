from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class KroonKycConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kroon_kyc'
    verbose_name = _("Kroon KYC")
