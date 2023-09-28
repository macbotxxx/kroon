from django.contrib import admin
from .models import Mask_Statement_Of_Account

# Register your models here.

@admin.register(Mask_Statement_Of_Account)
class Mask_Statement_Of_AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'masked_id')
    list_display_links = ('user', 'masked_id')
    readonly_fields = ('masked_id','start_date','end_date','created_date', 'modified_date', 'user')