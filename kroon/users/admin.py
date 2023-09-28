from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from .models import User,UserActivity, UserBankDetails, UserAddress, UserWrongPinValidate, UserActivity,KroonTermsAndConditions, BusinessProfile, PolicyAndCondition, KroonFQA, KioskFAQ
from rest_framework_simplejwt import token_blacklist
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)

@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin , admin.ModelAdmin):
    list_display = ('email', 'name', 'wallet_id','kroon_token','default_currency_id','account_type','created_date','last_login')
    list_display_links = ('email', 'name', 'wallet_id',)
    search_fields = ('email','wallet_id','account_type')
    list_filter = ('country_of_residence','account_type')
    # django export action
    export_order = ('email')

    
@admin.register(UserBankDetails)
class UserBankDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_name', 'account_number', 'bank_name', 'bank_code', 'bank_id')
    list_display_link = ('user', 'account_name', 'account_number', )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_or_flat_number','street_name','building_name', 'state', 'city', 'zip_post_code', )
    list_display_link = ('user', 'street_or_flat_number','street_name','building_name', 'state', 'city', 'zip_post_code', )


@admin.register(UserWrongPinValidate)
class UserWrongPinValidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'failed_password', 'banned')
    list_display_link = ('user', 'failed_password', 'banned')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'hostname', 'ip_address', 'created_date')
    list_display_link = ('user', 'hostname', 'ip_address','created_date')


@admin.register(KroonTermsAndConditions)
class KroonTermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('id','active','platform')
    list_display_link = ('id','active','platform')


@admin.register(PolicyAndCondition)
class PolicyAndConditionAdmin(admin.ModelAdmin):
    list_display = ('id','active','platform')
    list_display_link = ('id','active','platform')


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_id', 'business_name', 'business_contact_number', 'active', 'created_date')
    list_display_links = ('user', 'business_id', 'business_name', 'business_contact_number', 'active', 'created_date')


@admin.register(KroonFQA)
class KroonFQAAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_date', 'modified_date')
    list_display_links = ('question', 'created_date', 'modified_date')


@admin.register(KioskFAQ)
class KioskFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_date', 'modified_date')
    list_display_links = ('question', 'created_date', 'modified_date')