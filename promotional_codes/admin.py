from django.contrib import admin

from subscriptions.models import Subscription_Plan
from subscriptions.views import transaction_ref, transaction_ref_re
from .models import Government_Promo_Code,  Discount_Code
# Register your models here.

# generating promo code for kiosk_plus plan

@admin.action(description='Generate kiosk plus Monthly Promo Code')
def generate_kiosk_plus_monthly_code(modeladmin, request, queryset):
    code_range = 50
    plan = Subscription_Plan.objects.get( plan_name = "Kiosk Plus" )
    for i in range( code_range ):
        codes = transaction_ref()
        codes_re = transaction_ref_re()
        try:
            Government_Promo_Code.objects.get( promo_code = codes , used_code = False )
            Government_Promo_Code.objects.create( code_plan = plan , promo_code = codes_re )
        except Government_Promo_Code.DoesNotExist:
            Government_Promo_Code.objects.create( code_plan = plan , promo_code = codes )


@admin.action(description='Generate kiosk plus Yearly Promo Code')
def generate_kiosk_plus_yearly_code(modeladmin, request, queryset):
    code_range = 50
    plan = Subscription_Plan.objects.get( plan_name = "Kiosk Plus" )
    for i in range( code_range ):
        codes = transaction_ref()
        codes_re = transaction_ref_re()
        try:
            Government_Promo_Code.objects.get( promo_code = codes , used_code = False)
            Government_Promo_Code.objects.create( code_plan = plan , promo_code = codes_re , yearly_code = True )
        except Government_Promo_Code.DoesNotExist:
            Government_Promo_Code.objects.create( code_plan = plan , promo_code = codes , yearly_code = True )

# kiosk_plus plan_name

# start plus plus


@admin.action(description='Generate Kiosk Pro Monthly Promo Code')
def generate_kiosk_pro_monthly_code(modeladmin, request, queryset):
    code_range = 50
    plan = Subscription_Plan.objects.get( plan_name = "Kiosk Pro" )
    for i in range( code_range ):
        codes = transaction_ref()
        codes_re = transaction_ref_re()
        try:
            Government_Promo_Code.objects.get( promo_code = codes , used_code = False )
            Government_Promo_Code.objects.create( code_plan = plan , promo_code = codes_re )
        except Government_Promo_Code.DoesNotExist:
            Government_Promo_Code.objects.create( code_plan = plan , promo_code = codes )


@admin.action(description='Generate Kiosk Pro Yearly Promo Code')
def generate_kiosk_pro_yearly_code(modeladmin, request, queryset):
    code_range = 50
    plan = Subscription_Plan.objects.get( plan_name = "Kiosk Pro" )
    for i in range( code_range ):
        codes = transaction_ref()
        codes_re = transaction_ref_re()
        try:
            Government_Promo_Code.objects.get( promo_code = codes , used_code = False)
            Government_Promo_Code.objects.create( code_plan = plan , promo_code = codes_re , yearly_code = True )
        except Government_Promo_Code.DoesNotExist:
            Government_Promo_Code.objects.create( code_plan = plan , promo_code = codes , yearly_code = True )


@admin.action(description='Generate Subscription Discount Code')
def generate_Discount_Code(modeladmin, request, queryset):
    code_range = 50

    for i in range( code_range ):
        codes =  f"KGDC{transaction_ref()}"
        codes_re = f"KGDC{transaction_ref_re()}"
        try:
            Discount_Code.objects.get( discount_code = codes , used_code = False)
            Discount_Code.objects.create( discount_code = codes_re  )
        except Discount_Code.DoesNotExist:
            Discount_Code.objects.create( discount_code = codes  )
#start plus

@admin.register(Government_Promo_Code)
class Government_Promo_CodeAdmi(admin.ModelAdmin):
    list_display = ('code_plan', 'promo_code', 'used_code' , 'yearly_code' , 'user')
    list_display_links = ('code_plan', 'promo_code', 'used_code', 'yearly_code', 'user')
    readonly_fields = ['user',]

    actions = [generate_kiosk_plus_monthly_code, generate_kiosk_plus_yearly_code, generate_kiosk_pro_monthly_code, generate_kiosk_pro_yearly_code]
    # custommizing decorator

@admin.register(Discount_Code)
class Discount_CodeAdmi(admin.ModelAdmin):
    list_display = ('discount_code', 'used_code' , 'user')
    list_display_links = ('discount_code', 'used_code', 'user')
    readonly_fields = ['user',]

    actions = [generate_Discount_Code]

    