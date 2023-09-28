from django.contrib import admin
from .models import NewsFeed


@admin.register(NewsFeed)
class NewsFeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_date', 'modified_date')
    list_display_links = ('title', 'status', 'created_date', 'modified_date')
