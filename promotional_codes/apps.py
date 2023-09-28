from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PromotionalCodesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promotional_codes'
    verbose_name = _("Government Promo Codes")
