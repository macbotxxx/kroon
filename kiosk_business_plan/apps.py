from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KioskBusinessPlanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kiosk_business_plan'
    verbose_name = _('Merchant Business Plan')
