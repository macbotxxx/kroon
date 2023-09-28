from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from locations.models import Country
from kiosk_business_plan.models import Business_Plan , BusinessPlanExpenses
from kiosk_categories.models import Category 



class BusinessPlanExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPlanExpenses
        fields = ('expenses', 'expenses_amount')


class BusinessPlanFormSerializers(serializers.ModelSerializer):
    year_of_operation = serializers.DateField()
    business_expenses = BusinessPlanExpensesSerializer( many = True , required = False )
    class Meta:
        model = Business_Plan
        fields = ( 'business_category', 'year_of_operation', 'number_of_employees','business_expenses' ,'period_of_report')


class BusinessPlanIDSerializers(serializers.ModelSerializer):
    class Meta:
        model = Business_Plan
        fields = ('id', 'created_date', )
