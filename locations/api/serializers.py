from rest_framework import serializers
from locations.models import Country, Country_Province


class Country_ProvinceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country_Province
        fields = ('id','province')



class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"


class CountryDetails(serializers.ModelSerializer):

    class Meta:
        model = Country
        ref_name = "country_details"
        fields = ['id','name', 'iso2', 'native']



class FireBase (serializers.Serializer):
    device_ID = serializers.CharField()
