from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

OPT_CHIOCES = (
     ('kroon', _('Kroon')),
     ('kiosk', _('Kiosk')),
)

class EmailOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    platform = serializers.ChoiceField(choices=OPT_CHIOCES)
    

class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField( required = False )
    otp_pin = serializers.IntegerField()
