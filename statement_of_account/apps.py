from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatementOfAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'statement_of_account'
    verbose_name = _('statement of account')
