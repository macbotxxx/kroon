from django.contrib import admin
from .models import AdminPushNotifications

# Register your models here.
@admin.register(AdminPushNotifications)
class AdminPushNotificationsadmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_date')
    list_display_links = ('title', 'status', 'created_date')
