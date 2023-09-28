from django.contrib import admin
from .models import TaskTest
# Register your models here.

@admin.register(TaskTest)
class TaskTestAdmin(admin.ModelAdmin):
    list_display = ('created_date','content',)