from django.contrib import admin
from .models import AdminNewsFeed

# Register your models here.
@admin.register(AdminNewsFeed)
class AdminNewsFeedadmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_date')
    list_display_links = ('title', 'status', 'created_date')
