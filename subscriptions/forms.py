from django import forms
from django.utils.translation import gettext_lazy as _



class Gov_Promo_codeForm (forms.Form):
    promotional_code = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(Gov_Promo_codeForm, self).__init__(*args, **kwargs)
        self.fields['promotional_code'].widget.attrs['placeholder'] = _('promotional code')
        self.fields['promotional_code'].help_text = _('kindly input your promotional code provided by your government in the above form.')
