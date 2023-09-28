from django.contrib import admin
from .models import Onboarding_Users_CSV  , Action_logs ,Government_Organizations
# Register your models here.

@admin.register(Onboarding_Users_CSV)
class Onboarding_Users_CSVAdmin(admin.ModelAdmin):
    list_display = ('on_boarding_user', 'on_boarding_user_file', 'on_boarding_complete', 'on_boarding_complete_date')
    list_display_links = ('on_boarding_user',)


@admin.register( Action_logs )
class Action_logs_Admin(admin.ModelAdmin):
    list_display = ('user', 'action','created_date')
    list_display_links = ('user', 'action')


@admin.register( Government_Organizations )
class Government_Organizations_Admin(admin.ModelAdmin):
    list_display = ('government_organization',)
    list_display_links = ('government_organization',)
