from django import forms
from .models import Training_Cert



class Training_Cert_Form(forms.ModelForm):
    date_of_completion = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}))

    class Meta:
        model = Training_Cert
        fields = ('cert_bearer_first_name', 'cert_bearer_last_name', 'cert_bearer_country','date_of_completion', 'traning_platform')


class Cert_Number_form (forms.ModelForm):
     class Meta:
        model = Training_Cert
        fields = ('cert_number',)
