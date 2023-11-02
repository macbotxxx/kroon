from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminReportsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_reports"
    verbose_name = _("Admin Reports")
