from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KroonKioskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kroon_kiosk'
    verbose_name = _("Kroon Kiosk")
