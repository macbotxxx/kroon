from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VirtualCardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'virtual_cards'
    verbose_name = _('Virtual Cards')
