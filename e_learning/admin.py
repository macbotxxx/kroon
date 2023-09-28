from django.contrib import admin
from .models import Kiosk_E_Learning, App_Survey ,SurveyQA, AppSurveyQuestion
# Register your models here.

@admin.register(Kiosk_E_Learning)
class Kiosk_E_LearningAdmi(admin.ModelAdmin):
    list_display = ('title', 'vd_link')
    list_display_links = ('title', 'vd_link')



@admin.register( AppSurveyQuestion )
class AppSurveyQuestion_Admin(admin.ModelAdmin):
    list_display = ('survey_question',)
    list_display_links = ('survey_question',)


class SurveyQAInline(admin.TabularInline):
    model = SurveyQA
    fields = ('survey_qa', 'survey_questions_id', 'survey_answer')
    extra = 1


@admin.register(App_Survey)
class App_SurveyAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_display_links = ('user',)
    inlines = [SurveyQAInline]
