import string
import random
from decimal import Decimal
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , CreateAPIView, UpdateAPIView, ListCreateAPIView, GenericAPIView

# helpers 
from helpers.common.security import KOKPermission
from helpers.common.virtual_cards import Virtual_Card, kroon_method_virtual_card , verify_card_payment , kroon_fund_virtual_card , status_action_virtual_card


from payments.models import Payment_Topup
from payments.api.serializers import PaymentTopUpSerializer


from .serializers import Create_Virtual_Cards_Serializers , User_Virtual_Cards , Initiate_Payment_Serializer, Fund_Virtual_Card_Serializer , Card_Transaction_Serializer

from kroon_kyc.models import KycApplication , MarchantKycApplication

from virtual_cards.models import Virtual_Cards_Details , All_Cards_Transactions


# generating transactional id 
def transaction_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))


class Create_Virtual_Cards_View ( ListCreateAPIView ):
    """
    the virtual cards view set
    """
    permission_classes = [ IsAuthenticated , KOKPermission ]
    serializer_class = Create_Virtual_Cards_Serializers
    card_details = User_Virtual_Cards
    
    def get (self, request, *args, **kwargs):
        cards = Virtual_Cards_Details.objects.select_related('user').filter( user = self.request.user , is_active = True)
        serializer = self.card_details( cards, many=True )
        return Response({'status':'success', 'message':'Cards fetched successfully', 'data':serializer.data}, status=status.HTTP_200_OK )


    def post ( self, request, *args, **kwargs ):
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            payment_method = serializer.validated_data.get('payment_method')
            currency = serializer.validated_data.get('currency')
            payment_ref = serializer.validated_data.get('payment_ref')
            card_design = serializer.validated_data.get('card_design')

            try:

                # checking the kyc according to the user account type
                if request.user.account_type == "merchant":
                    MarchantKycApplication.objects.get( user = request.user )
                elif request.user.account_type == "personal":
                    KycApplication.objects.get( user = request.user )
                else:
                    pass

            except KycApplication.DoesNotExist:
                return Response({'status':'error', 'message':'Complete your KYC application to continue.'}, status=status.HTTP_404_NOT_FOUND)

            if payment_method == "kroon":
                # using kroon balance to create virtual card
                create_virtual_card_kroon = kroon_method_virtual_card( request , currency , card_design )
                response_status = create_virtual_card_kroon['status']
                message = create_virtual_card_kroon['message']
                data = create_virtual_card_kroon['data']

                # status code
                if response_status == 'success':
                    response_status_code = status.HTTP_201_CREATED
                else:
                    response_status_code = status.HTTP_400_BAD_REQUEST

                return Response({'status':response_status,'message':message, 'data':data}, status=response_status_code )


            elif payment_method == "card":
                # using card payment to create virtual card
                card_id = None 
                user_id = self.request.user.id
                create_virtual_card = verify_card_payment( payment_ref , currency , user_id , card_id , card_design )
                response_status = create_virtual_card['status']
                message = create_virtual_card['message']
                data = create_virtual_card['data']
                # status code
                if response_status == 'success':
                    response_status_code = status.HTTP_201_CREATED
                else:
                    response_status_code = status.HTTP_400_BAD_REQUEST

                return Response({'status':response_status,'message':message, 'data':data}, status=response_status_code )

            else:
                return Response({'status':'error', 'message':'Invalid payment method', 'data':''}, status=status.HTTP_400_BAD_REQUEST )

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class Virtual_Cards_Details_View ( ListAPIView ):
    permission_classes = [ IsAuthenticated , KOKPermission ]
    serializer_class = User_Virtual_Cards

    def get (self, request, *args, **kwargs):
        card_id = kwargs.get('card_id')
        try:
            card_details = Virtual_Cards_Details.objects.get( card_id = card_id )
        except Virtual_Cards_Details.DoesNotExist:
            return Response({'status':'error', 'message':'card details not found', 'data':''},  status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class( card_details )
        return Response({'status':'success','message':'card details fetched successfully', 'data':serializer.data}, status=status.HTTP_200_OK )



            
class Initiate_Payment (CreateAPIView):
    permission_classes = [ IsAuthenticated , KOKPermission ]
    serializer_class = Initiate_Payment_Serializer

    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class( data = request.data )
        transac_ref = f"KOK_VIRTUAL_CARD_{transaction_ref()}"

        if serializer.is_valid():
            amount = serializer.validated_data.get('amount')
            currency = serializer.validated_data.get('currency')
            serializer = Payment_Topup(
            payment_ref = transac_ref,
            user = request.user,
            amount_paid=Decimal(amount),
            currency = currency,
            action = "Virtual Card Payment Initiarization"
                )
            serializer.save()

            return Response({'status':'success','message':'Virtual card payment initiated','data':PaymentTopUpSerializer(serializer).data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Fund_Card_view (CreateAPIView):
    """
    This funds a specific virtual card
    """

    permission_classes = [ IsAuthenticated , KOKPermission ]
    serializer_class = Fund_Virtual_Card_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            card_id = kwargs.get('card_id')
            payment_method = serializer.validated_data.get('payment_method')
            amount = serializer.validated_data.get('amount')
            payment_ref = serializer.validated_data.get('payment_ref')
            currency = None
            user_id = self.request.user.id
            try:
                Virtual_Cards_Details.objects.get( card_id = card_id , is_active = True)
            except KeyError:
                response = {'status':'error', 'message':'card id is invalide or does not exist', 'data':''}
                return response

            # funding virtual card according to the payment method
            # using kroon and card payment method
            if payment_method == 'kroon':
                fund_virtual_card_response = kroon_fund_virtual_card(  amount , user_id , card_id )
                response_status = fund_virtual_card_response['status']
                message = fund_virtual_card_response['message']
                data = fund_virtual_card_response['data']

                # status code
                if response_status == 'success':
                    response_status_code = status.HTTP_201_CREATED
                else:
                    response_status_code = status.HTTP_400_BAD_REQUEST
                return Response({'status':response_status,'message':message, 'data':data}, status=response_status_code )

            elif payment_method == 'card':
                card_design = None
                # this topups the card using card payment method
                fund_virtual_card_response = verify_card_payment( payment_ref , currency , user_id , card_id , card_design )
                response_status = fund_virtual_card_response['status']
                message = fund_virtual_card_response['message']
                data = fund_virtual_card_response['data']

                # status code
                if response_status == 'success':
                    response_status_code = status.HTTP_201_CREATED
                else:
                    response_status_code = status.HTTP_400_BAD_REQUEST
                return Response({'status':response_status,'message':message, 'data':data}, status=response_status_code )
                
            else:
                return Response({'status':'error', 'message':'Invalid payment method', 'data':''}, status=status.HTTP_400_BAD_REQUEST )

        return Response(serializers.errors ,  status=status.HTTP_400_BAD_REQUEST)



class Block_Virtual_Card ( APIView ):
    """
    This call terminates a virtual card created by the User.

    **PATH PARAMS**

    **id**

    This is the id of the virtual card to be fetched. You can get this id from the call to create a virtual card or
    list virtual cards as data.id 
    
    **status_action**

    This is the action you want to perform on the virtual card. Can be **block** or **unblock**.
    """

    permission_classes = [ IsAuthenticated , KOKPermission ]

    def put (self, request, *args, **kwargs):
        card_id = kwargs.get('card_id')
        status_action = kwargs.get('status_action')
        # checking if the card_id exists
        try:
            Virtual_Cards_Details.objects.get( card_id = card_id , is_active = True )
        except KeyError:
            response = {'status':'error', 'message':'card id is invalide or does not exist', 'data':''}
            return response

        card_action = Virtual_Card()
        card_response = card_action.block_unblock_virtual_card( card_id , status_action )
        response_status = card_response['status']
        message = card_response['message']
        data = card_response['data']

        # status code
        if response_status == 'success':
            response_status_code = status.HTTP_201_CREATED
            status_action_virtual_card( card_id , status_action )
        else:
            response_status_code = status.HTTP_400_BAD_REQUEST
        return Response({'status':response_status,'message':message, 'data':data}, status=response_status_code )



class Terminate_Virtual_Card ( APIView ):

    """
    terminates a virtual card

    **Terminate A Virtual Card**

    This call terminates a virtual card created by the User.

    **PATH PARAMS**

    **id**

    This is the card_id of the virtual card to be fetched. You can get this id from the call to create a virtual card or list virtual cards as card_id
    """
    permission_classes = [ IsAuthenticated , KOKPermission ]

    def put (self, request, *args, **kwargs):
        card_id = kwargs.get('card_id')
        status_action = "terminate"
        # checking if the card_id exists
        try:
            Virtual_Cards_Details.objects.get( card_id = card_id , is_active = True )
        except Virtual_Cards_Details.DoesNotExist:
            return Response({'status':'error', 'message':'Unable to retrieve the requested card.', 'data':''}, status=status.HTTP_404_NOT_FOUND)

        card_action = Virtual_Card()
        card_response = card_action.terminate_virtual_card( card_id  )
        response_status = card_response['status']
        message = card_response['message']
        data = card_response['data']

        # status code
        if response_status == 'success':
            response_status_code = status.HTTP_201_CREATED
            status_action_virtual_card( card_id , status_action )
        else:
            response_status_code = status.HTTP_400_BAD_REQUEST
        return Response({'status':response_status,'message':message, 'data':data}, status=response_status_code )



class Card_Transaction ( APIView ):
    """
    This call fetches transactions by date range on a single card

    **Get A Virtuals Card's Transactions**

    This call fetches transactions by date range on a single card

    **PATH PARAMS**

    **id**

    This is the card_id of the virtual card to be fetched. You can get this id from the call to create a virtual card or list virtual cards as card_id
    """

    permission_classes = [ IsAuthenticated , KOKPermission ]
    serializer_class = Card_Transaction_Serializer

    def get( self, request, *args, **kwargs):
        card_id = kwargs.get('card_id')
        # checking if the card_id exists
        try:
            Virtual_Cards_Details.objects.get( card_id = card_id , is_active = True )
        except Virtual_Cards_Details.DoesNotExist:
            return Response({'status':'error', 'message':'Unable to retrieve the requested card.', 'data':''}, status=status.HTTP_404_NOT_FOUND)

        transactions = All_Cards_Transactions.objects.select_related('user').filter( card_id = card_id ).order_by('-created_date',)[:15]
        serializer = self.serializer_class( transactions , many = True )
        return Response({'status':'success', 'message':'card transactions fetched successfully', 'data':serializer.data}, status=status.HTTP_200_OK)
        

        



