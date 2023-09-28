from rest_framework import serializers
from ads.models import Ads


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ['ad_name','ad_image', 'ad_url',]
       