from django.contrib import admin
from .models import Country, Language , Country_Province

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name' , 'iso2','currency','phone_code','accept_signup', 'banned', 'created_date', 'modified_date')
    list_display_links = ('name' , 'iso2','currency','phone_code', 'created_date', 'modified_date')


@admin.register(Country_Province)
class Country_ProvinceAdmin(admin.ModelAdmin):
    list_display = ('country', 'province', 'active', 'created_date', 'modified_date')
    list_display_links = ('country', 'province', 'active', 'created_date', 'modified_date')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language_name', 'language_ISO2')
    list_display_link = ('language_name', 'language_ISO2')
