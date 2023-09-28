from rest_framework import  status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from helpers.common.security import KOKPermission , KOKMerchantOnly
from .serializers import Government_Organizations_Serializer
from gov_panel.models import Government_Organizations

class ListGovOrgs (ListAPIView):
    permission_classes = [ KOKPermission , AllowAny,]
    queryset = Government_Organizations.objects.all()
    serializer_class = Government_Organizations_Serializer

