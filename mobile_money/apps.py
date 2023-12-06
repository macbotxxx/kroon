from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MobileMoneyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mobile_money'
    verbose_name = _("Mobile Money")


