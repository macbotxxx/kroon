from django.contrib import admin
from .models import Generate_Pin

# Register your models here.
@admin.register(Generate_Pin)
class Generate_Pin_Admin(admin.ModelAdmin):
    list_display = ('user', 'pin')
    list_display_links = ('user', 'pin')
