from django.urls import path
from . import views

urlpatterns = [
    path('kiosk-e-learning/', views.Kiosk_E_Learning_View.as_view(), name='kiosk_e_learning'),
    path('app-survey/', views.AppSubmiSurvey.as_view()),
    path('list-survey-ques/', views.ListSurveyQuestions.as_view()),
]