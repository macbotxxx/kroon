from django.contrib import admin
from .models import Training_Cert


# Register your models here.
@admin.register(Training_Cert)
class Training_CertAdmin(admin.ModelAdmin):
    list_display = ('user', 'cert_number', 'cert_bearer_first_name', 'cert_bearer_last_name')
    list_display_links = ('user', 'cert_number', 'cert_bearer_first_name', 'cert_bearer_last_name')
