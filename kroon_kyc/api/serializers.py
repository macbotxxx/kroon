from rest_framework import serializers
from kroon_kyc.models import KycApplication, MarchantKycApplication

class KYCSerializer(serializers.ModelSerializer):

    class Meta:
        model = KycApplication
        exclude = ["user","created_date", "modified_date", "kyc_status", "kyc_refused_code",]
        

class MarchantKycApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarchantKycApplication
        fields ="__all__"
        read_only_fields = ["user","created_date", "modified_date", "kyc_status", "kyc_refused_code",]