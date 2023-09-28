from datetime import timedelta
import string
import random


from decimal import Decimal
from helpers.common.security import KOKPermission
from kroon.users.models import User

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404


# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from payments.models import Payment_Topup
from helpers.common.payment import Etransac

from .serializers import PaymentTopUpSerializer, PaymentTopUpVerificationSerializer,CancelPaymentRequestSerializer

from transactions.models import Transactions

from django.conf import settings


FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY
FCM_SERVER_KEY = settings.FCM_SERVER_KEY

etransac = Etransac()


def transaction_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))


class TopUpPaymentView (CreateAPIView):
    """
    wallet topup payment view 
    """
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = PaymentTopUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = PaymentTopUpSerializer(data=request.data)
        transac_ref = f"KROON_{transaction_ref()}"

        if serializer.is_valid():
            amount_paid=serializer.data.get('amount_paid')
            amount_in_kroon = serializer.data.get('amount_in_kroon')
            

            if settings.USE_ETRANSAC:    
                initialize_payment = etransac.payment_initialize(
                    amount = Decimal(amount_paid),
                    payment_refrence = transac_ref,
                    customer_first_name = self.request.user.first_name,
                    customer_last_name = self.request.user.last_name,
                    customer_email = self.request.user.email,
                    customer_contact_number = self.request.user.contact_number,
                )

                payment_link = initialize_payment['authorizationUrl']
                payment_ref = initialize_payment['reference']
                credo_ref = initialize_payment['credoReference']

            serializer = Payment_Topup(
            payment_ref = payment_ref,
            user = request.user,
            amount_paid=Decimal(amount_paid),
            amount_in_kroon = Decimal(amount_in_kroon),
            currency = request.user.default_currency_id,
            payment_link = payment_link,
            etransac_ref = credo_ref
                )
            serializer.save()
        
            # Recipient Transactional Record History
            Transactions.objects.create(user = request.user ,  recipient = request.user,amount = amount_in_kroon,transactional_id = payment_ref,amount_in_localcurrency = amount_paid, currency = 'KC',local_currency = request.user.default_currency_id, narration = f'kroon wallet topup using CARD PAYMENT',action = 'KROON WALLET TOPUP', status = 'pending',  kroon_balance = request.user.kroon_token)

            return Response({'status':'success','message':'Topup payment initiated','data':PaymentTopUpSerializer(serializer).data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class TopUpPaymentVerification (CreateAPIView):
    """
    wallet topup payment verification
    """
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = PaymentTopUpVerificationSerializer

    def post (self, request, *args, **kwargs):
        serializer = PaymentTopUpVerificationSerializer(data=request.data)
        user_currency = request.user.default_currency_id
        if serializer.is_valid():
            payment_ref = serializer.data.get('payment_ref')
            amount_paid = serializer.data.get('amount_paid')
            
            # shedule the user country 
            # country = ['Nigeria']
            # if str(request.user.country_of_residence) in country: 
            #     payment = get_object_or_404(Payment_Topup, payment_ref=payment_ref)
            #     verified = payment.verify_payment_paystack()
            # else:
            
            payment = get_object_or_404(Payment_Topup, payment_ref=payment_ref)
            verified = payment.verify_payment_flutterwave()
            
            if verified:
                validating_account = Payment_Topup.objects.get(payment_ref=payment_ref)
                if validating_account.settled:
                    return Response({'status':'error','message':'the above payment has already been settled',},  status=status.HTTP_404_NOT_FOUND)

                if validating_account.amount_paid != Decimal(amount_paid):
                    return Response({'status':'error','message':'not the same amount with the initial amount referenced to the transactional ID',},  status=status.HTTP_404_NOT_FOUND)

                if validating_account.status == 'successful':
                    """
                    taking process if the transaction is successful 
                    processes like toping the user account kroon balance and
                    also sending email to the user when its been handled 
                    """

                    user_token = User.objects.get(id = request.user.id)
                    # token = TokenRate.objects.get(currency__currency=user_currency)
                    # token_rate  = int(token.token_rate) * int(amount_paid)
                    user_token.kroon_token += Decimal(payment.amount_in_kroon)
                    user_token.save()

                    transactional_history = Transactions.objects.get(transactional_id = payment_ref )
                    transactional_history.kroon_balance = user_token.kroon_token
                    transactional_history.credited_kroon_amount = Decimal(payment.amount_in_kroon)
                    transactional_history.save()

                    payment.settled = True
                    payment.save()

                    # email notification for topup_payment
                    subject = 'Kroon Wallet TopUp Was Successful'
                    html_message = render_to_string(
                        'emails/topup.html',
                        {
                        'user': request.user,
                        'amount':amount_paid,
                        'payment':payment,
                        'currency':user_currency,
                        # 'token_rate': token.token_rate,
                        'token': payment.amount_in_kroon,
                        'transaction_ref':payment_ref,
                        } 
                    )
                    plain_message = strip_tags(html_message)
                    from_email = f"{settings.EMAIL_HOST_USER}" 
                    to = request.user.email
                    mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)

                    return Response({'status':'success','message':'user topup is sucessfully verified and completed','data':serializer.data, }, status=status.HTTP_201_CREATED)

                elif validating_account.status == 'pending':
                    return Response({'status':'success','message':'user topup is on pending ... it will be automatically been updated when the charge is been paid','data':serializer.data, }, status=status.HTTP_201_CREATED)
                
            return Response({'status':'error', 'message':'Invalid payment'},  status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)





class CancelPaymentRequest(CreateAPIView):

    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = CancelPaymentRequestSerializer
    serializer_details = PaymentTopUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            payment_ref = serializer.validated_data.get('payment_ref')
            update_payment = Payment_Topup.objects.get(payment_ref = payment_ref)
            update_payment.status = 'cancelled'
            update_payment.save()

            transactional_history = Transactions.objects.get(transactional_id = payment_ref )
            transactional_history.status = 'cancelled'
            transactional_history.kroon_balance = request.user.kroon_token
            transactional_history.save()

            return Response({'status':'success', 'message':'transaction has been cancelled','data':self.serializer_details(update_payment).data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


