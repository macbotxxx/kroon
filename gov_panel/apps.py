from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GovPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gov_panel'
    verbose_name = _("Gov Panel Onboarding")
