from locale import currency
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView , CreateAPIView, get_object_or_404
from rest_framework.views import APIView

from helpers.common.security import KOKPermission

from .serializers import TokenRateSerializer,PurchaseTokenFeesSerializer,WithDrawTokenFeesSerializer

from kroon_token.models import TokenRate, PurchaseTokenFees, WithDrawTokenFees
from locations.models import Country





class FeesAndVatFeesView (APIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializers_class = PurchaseTokenFeesSerializer
    token_serializer = TokenRateSerializer

    def get (self, request, *args, **kwargs):
        # getting the user country 
        user_country = Country.objects.get(name = request.user.country_of_residence)
        user_currency = Country.objects.get(currency = request.user.default_currency_id)
        try:
            token_rate = TokenRate.objects.get(currency = user_currency)
        except:
            return Response({'status':'error','message':'ether the country rate is not inputted , contact the customer service',}, status=status.HTTP_400_BAD_REQUEST)
            
        withqs = WithDrawTokenFees.objects.filter(country = user_country)
        purchaseqs = PurchaseTokenFees.objects.filter(country = user_country)
        purchaseserializers = PurchaseTokenFeesSerializer(purchaseqs, many=True)
        withdrawserializers = WithDrawTokenFeesSerializer(withqs, many=True)
        token_rate = self.token_serializer(token_rate)
       
        return Response({'status':'success','message':'this consists of both application fees , vat fees and token rate','top_up_rate':purchaseserializers.data, 'withdrawal_rate':withdrawserializers.data, 'token_rate':token_rate.data}, status=status.HTTP_202_ACCEPTED)

