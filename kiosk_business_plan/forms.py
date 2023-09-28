from django import forms
from django.utils.translation import gettext_lazy as _
from locations.models import Country
from .models import Business_Plan
from kiosk_categories.models import Category 


class BusinessPlanForm(forms.ModelForm):
    year_of_operation = forms.DateField(widget=forms.TextInput(
        attrs={
        'class':' date-picker',
        }
    ))

    business_category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        # empty_label=_('Country of Residence'),
        help_text=_('this shows the business category '))

    class Meta:
        model = Business_Plan
        fields = ( 'business_category', 'year_of_operation', 'number_of_employees', 'salaries', 'electricity', 'data', 'fuel', 'period_of_report')
        
