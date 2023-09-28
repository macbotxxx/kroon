from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KioskOfflineModeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kiosk_offline_mode'
    verbose_name = _('Kiosk offline Mode')
