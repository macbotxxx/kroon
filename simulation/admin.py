from django.contrib import admin
from .models import Simulate_Account

# Register your models here.
@admin.register(Simulate_Account)
class Simulate_AccountAdmin(admin.ModelAdmin):
    list_display = ('country_iso2', 'number_of_merchants','action_count', 'submitted','completed','processing_status')
    list_display_links = ('country_iso2', 'number_of_merchants','action_count', 'submitted','completed','processing_status')