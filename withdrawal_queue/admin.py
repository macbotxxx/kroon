from django.contrib import admin
from .models import Test_Models
# Register your models here.

@admin.register(Test_Models)
class Test_ModelsAdmin(admin.ModelAdmin):
    list_display = ('created_date','content',)