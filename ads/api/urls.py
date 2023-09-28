from django.urls import path
from . import views
# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='Kroon Network Ads')
app_name = "Kroon Network Ads"

app_name = "Kroon Network Ads"
urlpatterns =[
    path('ads/<str:platform>/' , views.AdsView.as_view())
]