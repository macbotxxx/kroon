from django.contrib import admin
from .models import Ads

# Register your models here.

@admin.register(Ads)
class AdsAdmin (admin.ModelAdmin):
    list_display = ('ad_name', 'ad_image', 'ad_url',  'active')
    list_display_links = ('ad_name', 'ad_image', 'ad_url',  'active')