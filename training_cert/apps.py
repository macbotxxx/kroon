from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TrainingCertConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training_cert'
    verbose_name=_("Training Certificate")
