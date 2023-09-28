
from django.contrib import admin
from .models import Subscription_Plan , Merchant_Subcribers
# Register your models here.




@admin.register(Subscription_Plan)
class Subscription_PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'plan_fee', 'plan_duration', 'plan_default_currency', 'active')
    list_display_links = ('plan_name', 'plan_fee', 'plan_duration', 'plan_default_currency', 'active')
    


@admin.register(Merchant_Subcribers)
class Merchant_SubcribersAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date','sub_plan_id', 'end_date', 'active')
    list_display_links = ('user', 'plan', 'start_date','sub_plan_id', 'end_date', 'active')