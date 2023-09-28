from django.contrib import admin
from .models import KroonGift
# Register your models here.

@admin.register(KroonGift)
class KroonGiftAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'amount','settled', 'created_date')
    list_display_links = ('user', 'email', 'amount','settled', 'created_date')
