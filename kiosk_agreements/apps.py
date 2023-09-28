from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KioskAgreementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kiosk_agreements"
    verbose_name = _("Kiosk Agreement")

