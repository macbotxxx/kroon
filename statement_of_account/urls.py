from django.urls import path
from . import views

app_name = 'statement'

urlpatterns = [
    path('download-pdf/<str:id>/', views.statement_of_account_view, name='statement_of_account'),
    path('pdf-file', views.render_pdf_view, name='generate_pdf'),
    path('test/', views.test_view, name='test'),
]