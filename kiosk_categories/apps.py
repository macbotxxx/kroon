from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class KioskCategoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kiosk_categories'
    verbose_name = _("Kiosk Categories")
