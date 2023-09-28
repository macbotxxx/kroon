from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KroonGiftConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kroon_gift'
    verbose_name = _('Gift Kroon Records')
