from django.contrib import admin
from .models import KycApplication, MarchantKycApplication
# Register your models here.

@admin.register(KycApplication)
class KycApplication(admin.ModelAdmin):
    list_display = ('legal_first_names', 'legal_last_names', 'birth_date', 'kyc_status', 'created_date', 'modified_date',)
    list_display_links = ('legal_first_names', 'legal_last_names', )


@admin.register(MarchantKycApplication)
class MarchantKycApplicationAdmi(admin.ModelAdmin):
    list_display = ('legal_first_names', 'legal_last_names', 'birth_date', 'kyc_status', 'created_date', 'modified_date',)
    list_display_links = ('legal_first_names', 'legal_last_names', )