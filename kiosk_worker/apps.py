from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class KioskWorkerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kiosk_worker'
    verbose_name = _('kiosk Workers Account')
