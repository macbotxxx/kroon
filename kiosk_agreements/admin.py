from django.contrib import admin
from .models import Business_Agreements , Agreements_Info , Shares_Signatures , Shares_Agreements , Goods_And_Services_Agreement , Loan_Agreement


# Register your models here.

@admin.register(Business_Agreements)
class Business_AgreementsAdmin(admin.ModelAdmin):
    list_display = ('document', 'document_thumbnail', 'document_file', 'active')
    list_display_links = ('document', 'document_thumbnail', 'document_file', 'active')



@admin.register(Agreements_Info)
class Agreements_InfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'industry', 'business_logo', 'business_owner_name', 'business_address')
    list_display_links = ('user', 'business_name', 'industry', 'business_logo', 'business_owner_name', 'business_address')


@admin.register(Shares_Signatures)
class Shares_SignaturesAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'share', 'share_price')
    list_display_links = ('name', 'address', 'share', 'share_price')

@admin.register(Shares_Agreements)
class Shares_AgreementsAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_country', 'company_share')
    list_display_links = ('user', 'company_name', 'company_country', 'company_share')

@admin.register(Goods_And_Services_Agreement)
class Goods_And_Services_AgreementAdmin(admin.ModelAdmin):
    list_display = ('user', 'seller_name', 'seller_address')
    list_display_links = ('user', 'seller_name', 'seller_address')

@admin.register(Loan_Agreement)
class Loan_AgreementAdmin(admin.ModelAdmin):
    list_display = ('user', 'borrower_name', 'lender_name', 'amount')
    list_display_links = ('user', 'borrower_name', 'lender_name', 'amount')
    