from django.contrib import admin
from .models import OPTs

# Register your models here.
@admin.register(OPTs)
class OptsAdmin(admin.ModelAdmin):
    list_display = ( 'email','otp_code', 'duration', 'active')
    list_display_link = ( 'email','otp_code', 'duration', 'active')
