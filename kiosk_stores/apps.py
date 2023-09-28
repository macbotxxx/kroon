from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class KioskStoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kiosk_stores'
    verbose_name = _("Kiosk Merchant Products ")
