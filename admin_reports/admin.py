from django.contrib import admin
from .models import AdminPushNotifications

# Register your models here.
@admin.register(AdminPushNotifications)
class AdminPushNotificationsadmin(admin.ModelAdmin):
    list_display = ('title', 'device_id', 'status', 'created_at')
    list_display_links = ('title', 'device_id', 'status', 'created_at')
