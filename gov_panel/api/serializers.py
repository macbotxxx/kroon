from rest_framework import serializers
from gov_panel.models import Government_Organizations



class Government_Organizations_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Government_Organizations
        fields = ['id','government_organization']

