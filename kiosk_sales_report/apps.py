from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KioskSalesReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kiosk_sales_report'
    verbose_name = _("Kiosk Sales Report")
