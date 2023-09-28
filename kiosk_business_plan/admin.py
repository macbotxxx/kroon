from django.contrib import admin
from .models import Business_Plan , BusinessPlanExpenses


@admin.register(Business_Plan)
class BusinessPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'business_registration_number', 'business_contact')
    list_display_links = ('user', 'business_name', 'business_registration_number', 'business_contact')

# Register your models here.
@admin.register(BusinessPlanExpenses)
class BusinessPlanExpensesAdmin(admin.ModelAdmin):
    list_display = ('user', 'expenses', 'expenses_amount')
    list_display_links = ('user', 'expenses', 'expenses_amount')
