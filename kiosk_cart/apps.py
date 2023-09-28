from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KioskCartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kiosk_cart'
    verbose_name = _("Kiosk Cart And Checkout")
