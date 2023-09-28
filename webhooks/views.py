from decimal import Decimal
from django.shortcuts import render

# Create your views here.
import datetime as dt
import json
from secrets import compare_digest
import requests

from datetime import timedelta, datetime
from django.conf import settings
from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from rest_framework.response import Response
from django.core.mail import send_mail


# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading

from kroon.users.models import User

# import webhook_events
from kroon_withdrawal.models import Kroon_Withdrawal_Record
from transactions.models import Transactions
from payments.models import Payment_Topup
from subscriptions.models import Merchant_Subcribers , Subscription_Plan

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY



@csrf_exempt
@require_POST
@non_atomic_requests
def flutter_webhook( request ):
    given_token = request.headers.get("verif-hash", "")
    if not compare_digest(given_token, settings.KROON_WEBHOOK_HASH):
        msg = {'status':'error','message':'you are not authorized to make this push request.' }
        return JsonResponse(status=404,data=msg, safe=False)

    # Load the event data from JSON
    response_data = json.loads(request.body)
  
    # converting the dot from the event to underscore 
    try:
        dot_event  = response_data['event']
        event = dot_event.replace('.', '_')
        print(event)
    except:
        msg = {'status':'error','message':'you are not authorized to make this push request.' }
        return JsonResponse(status=404,data=msg, safe=False)

    # # getting the transaction id and verifying if the transaction is valid or not
    transaction_id = response_data['data']['id']


    # checking for the webhook events 

    if event == 'transfer_completed':
        """
        this section hold the webhook section for bank withdrawals 
        which is will update the database when ever a verified push notification
        is been sent by the third part. ( which at this case its flutterwave )
        transfer.complete events is been handled here 
        """
        
        url = f"https://api.flutterwave.com/v3/transfers/{transaction_id}"

        payload={}  
        headers = {
        'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}',
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response_data = response.json()

        status_pay = response_data['status']

        if status_pay == "success":
            reference = response_data['data']['reference']
            status_res = response_data['data']['status']
            narration = response_data['data']['complete_message']
            status = status_res.lower()

            if status == "successful":

                try:
                    withdrawal_records = Kroon_Withdrawal_Record.objects.get(reference=reference, transaction_id = transaction_id)

                except Kroon_Withdrawal_Record.DoesNotExist:
                    msg = {'status':'error','message':'Transaction does not exist on our database.'}
                    return JsonResponse(status=404,data=msg, safe=False)

                if  withdrawal_records.status == 'successful':
                    msg = {'status':'error','message':'Transaction has already been handled.'}
                    return JsonResponse(status=404,data=msg, safe=False)

                withdrawal_records.status = status
                withdrawal_records.settled = True
                withdrawal_records.save()

                transaction_update = Transactions.objects.get( transactional_id = reference , status = "processing" )
                transaction_update.status = status
                transaction_update.save()

                msg = {'status':'success','message':'transaction has been updated and recorded successfully.'}
                return JsonResponse(status=404,data=msg, safe=False)

            elif status == "failed":

                try:
                    withdrawal_records = Kroon_Withdrawal_Record.objects.get(reference=reference, transaction_id = transaction_id)
                    
                except Kroon_Withdrawal_Record.DoesNotExist:
                    msg = {'status':'error','message':'Transaction does not exist on our database.'}
                    return JsonResponse(status=404,data=msg, safe=False)

                if  withdrawal_records.status == 'failed':
                    msg = {'status':'error','message':'Transaction has already been handled.'}
                    return JsonResponse(status=404,data=msg, safe=False)

                withdrawal_records.status = status
                withdrawal_records.save()
                transaction_update = Transactions.objects.get(transactional_id = reference)
                transaction_update.status = status
                transaction_update.narration = narration
                transaction_update.save()
                
                # REFUNDING THE KROON FUNDS TO THE USERS
                user_record = User.objects.get( id = withdrawal_records.user.id )  
                user_record.kroon_token += transaction_update.debited_kroon_amount
                user_record.save()

                # SAVING THE TRANSACTIONAL History
                # Recipient Transactional Record History
                Transactions.objects.create(user = user_record , benefactor = user_record ,amount = Decimal(transaction_update.debited_kroon_amount) ,transactional_id = reference, currency = 'KC',local_currency = user_record.default_currency_id ,amount_in_localcurrency = transaction_update.amount_in_localcurrency, narration = 'LOCAL BANK WITHDRAWAL REFUND',action = 'LOCAL BANK WITHDRAWAL', status = 'successful', kroon_balance = user_record.kroon_token, credited_kroon_amount = Decimal(transaction_update.debited_kroon_amount) )

                msg = {'status':'success','message':'transaction has been updated and recorded successfully.'}
                return JsonResponse(status=201,data=msg, safe=False)

        
    elif event == 'charge_completed':
        """
        the charge webhook notification is been sent from the third party providers
        to notify us when ever a charge has taken place which this action will 
        automatically update our transactional table.
        """

        url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"

        payload={}  
        headers = {
        'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}',
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response_data = response.json()

        status_pay = response_data['status']
       

        if status_pay == "success":
            tx_ref = response_data['data']['tx_ref']
            status_res = response_data['data']['status']
            payment_type = response_data['data']['payment_type']
            created_at = response_data['data']['created_at']
            amount_settled = response_data['data']['amount_settled']

            # converting the payment response to lower case
            status_lower = status_res.lower()
            payment_type = payment_type.lower()
            
            if status_lower == 'successful':

                try:
                    transaction_record = Transactions.objects.get(transactional_id=tx_ref)
                except Transactions.DoesNotExist:
                    msg = {'status':'error','message':'Transaction does not exist on our database.'}
                    return JsonResponse(status=404,data=msg, safe=False)

                # getting the payment ref from the databases
                try:
                    payment_record = Payment_Topup.objects.get(payment_ref = tx_ref )
                except Transactions.DoesNotExist:
                    msg = {'status':'error','message':'Transaction does not exist on our database.'}
                    return JsonResponse(status=404,data=msg, safe=False)

                if transaction_record.status == 'successful':
                    msg = {'status':'error','message':'Transaction has already been handled.'}
                    return JsonResponse(status=404,data=msg, safe=False)

                elif transaction_record.status == 'pending':

                    # updating the payment ref from the payment table
                    payment_record.settled = True
                    payment_record.status = status_lower

                    # updating the users kron wallet 
                    user_token = User.objects.get(id = payment_record.user.id )
                    user_token.kroon_token += Decimal(payment_record.amount_in_kroon)
                    user_token.save()

                    # updating the transactional table 
                    transaction_record.kroon_balance = user_token.kroon_token
                    transaction_record.credited_kroon_amount = Decimal(payment_record.amount_in_kroon)
                    transaction_record.amount_settled = amount_settled
                    transaction_record.status = status_lower
                    transaction_record.save()

                    # this saves the payment record 
                    payment_record.save()

                    # email notification for topup_payment
                    subject = 'Kroon Wallet TopUp Was Successful'
                    html_message = render_to_string(
                        'emails/topup.html',
                        {
                        'user': payment_record.user,
                        'amount':payment_record.amount_paid,
                        'payment':payment_record.payment_method,
                        'currency':payment_record.currency,
                        # 'token_rate': token.token_rate,
                        'token': payment_record.amount_in_kroon,
                        'transaction_ref':payment_record.payment_ref,
                        } 
                    )
                    plain_message = strip_tags(html_message)
                    from_email = f"{settings.EMAIL_HOST_USER}" 
                    to = payment_record.user.email
                    mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)


                    msg = {'status':'success','message':'transaction has been updated and recorded successfully.'}
                    return JsonResponse(status=201,data=msg, safe=False)
                                
            elif status_lower == 'failed':
                # verifying the transaction record
                try:
                    transaction_record = Transactions.objects.get(transactional_id=tx_ref)
                except Transactions.DoesNotExist:
                    msg = {'status':'error','message':'Transaction does not exist on our database.'}
                    return JsonResponse(status=404,data=msg, safe=False)

                # updating the db when its failed
                transaction_record.status = status_lower
                transaction_record.save()

                # getting the payment ref from the databases
                try:
                    payment_record = Payment_Topup.objects.get(payment_ref = tx_ref )
                except Transactions.DoesNotExist:
                    msg = {'status':'error','message':'Transaction does not exist on our database.'}
                    return JsonResponse(status=404,data=msg, safe=False)
                
                # updating the payment ref from the payment table
                payment_record.settled = False
                payment_record.status = status_lower
                payment_record.save()

                msg = {'status':'success','message':'transaction has been updated and recorded successfully.'}
                return JsonResponse(status=201,data=msg, safe=False)
                
        else:
            pass

        msg = {'status':'error','message':'Transaction does not exist on our database.'}
        return JsonResponse(status=404,data=msg, safe=False)

    msg = {'status':'error','message':'Transaction does not exist on our database.'}
    return JsonResponse(status=404,data=msg, safe=False)



@csrf_exempt
@require_POST
@non_atomic_requests
def paystack_webhook ( request ):
    # Load the event data from JSON
    try:
        response_data = json.loads(request.body)
    except:
        msg = {'status':'error','message':'you are not authorized to make this push request.' }
        return JsonResponse(status=404,data=msg, safe=False)
  
    # converting the dot from the event to underscore 
    try:
        dot_event  = response_data['event']
        event = dot_event.replace('.', '_')
    except:
        msg = {'status':'error','message':'you are not authorized to make this push request.' }
        return JsonResponse(status=404,data=msg, safe=False)

    # # getting the transaction id and verifying if the transaction is valid or not
    transaction_id = response_data['data']['reference']

    if event == 'transfer_success':
        """
        this section hold the webhook section for bank withdrawals 
        which is will update the database when ever a verified push notification
        is been sent by the third part. ( which at this case its paystack )
        transfer.complete events is been handled here 
        """
        
        url = f"https://api.paystack.co/transfer/verify/{transaction_id}"

        payload={}  
        headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response_data = response.json()
        print(response_data)
        status_pay = response_data['status']
        reference = response_data['data']['reference']
        transfer_id = response_data['data']['transfer_code']

        print(reference, transfer_id)

        if status_pay:
          
            try:
                withdrawal_records = Kroon_Withdrawal_Record.objects.get( paystack_reference = reference , transaction_id = transfer_id)

            except Kroon_Withdrawal_Record.DoesNotExist:
                msg = {'status':'error','message':'Transaction does not exist on our database.'}
                return JsonResponse(status=404,data=msg, safe=False)

            if  withdrawal_records.status == 'successful':
                msg = {'status':'error','message':'Transaction has already been handled.'}
                return JsonResponse(status=404,data=msg, safe=False)

            withdrawal_records.status = status_pay
            withdrawal_records.status = "successful"
            withdrawal_records.is_approved = True
            withdrawal_records.settled = True
            withdrawal_records.save()

            transaction_update = Transactions.objects.get( transactional_id = withdrawal_records.reference , status = "processing" )
            transaction_update.status = "successful"
            transaction_update.save()

            msg = {'status':'success','message':'transaction has been updated and recorded successfully.'}
            return JsonResponse(status=404,data=msg, safe=False)

        else:
            msg = {'status':'error','message':'working.' }
            return JsonResponse(status=404,data=msg, safe=False)


@csrf_exempt
@require_POST
@non_atomic_requests
def paypal_webhook ( request ):
    # Load the event data from JSON
    try:
        response_data = json.loads(request.body)
    except:
        msg = {'status':'error','message':'you are not authorized to make this push request.' }
        return JsonResponse(status=404,data=msg, safe=False)

    # converting the dot from the event to underscore 
    try:
        dot_event  = response_data['event_type']
        event = dot_event.replace('.', '_')
        print( event )
    except:
        msg = {'status':'error','message':'you are not authorized to make this push request.' }
        return JsonResponse(status=404,data=msg, safe=False)

    # its been called when the renewal payment is failed
    # due to insufficent balance or block | expired card 
    
    if event == 'BILLING_SUBSCRIPTION_PAYMENT_FAILED':
        sub_id = response_data['resource']['id']
        sub_plan_id = response_data['resource']['plan_id']
        data_id = response_data['id']
        
        # updating the subscription record 
        try:
            user_sub = Merchant_Subcribers.objects.get( sub_plan_id = sub_plan_id , subscription_id = sub_id, recurring_payment = True , active = True)
        except Merchant_Subcribers.DoesNotExist :
            return JsonResponse(status=404,data={}, safe=False)

        user_sub.recurring_payment = False
        user_sub.active = False
        user_sub.save()

        msg = {'status':'success','message':'request handled successfully' }
        return JsonResponse(status=202,data=msg, safe=False)

    elif event == 'BILLING_SUBSCRIPTION_UPDATED':
        sub_id = response_data['resource']['id']
        sub_plan_id = response_data['resource']['plan_id']
        data_id = response_data['id']
        
        # updating the subscription record 
        try:
            user_sub = Merchant_Subcribers.objects.get( sub_plan_id = sub_plan_id , subscription_id = sub_id )
        except Merchant_Subcribers.DoesNotExist :
            return JsonResponse(status=404,data={}, safe=False)
        
        # getting details for the plan
        plan_info = Subscription_Plan.objects.get( id = user_sub.plan_id )
        if user_sub.yearly_plan:
            duration = plan_info.yearly_plan_duration
        else:
            duration = plan_info.plan_duration
            
        end_date = datetime.now()+timedelta( days = duration )
        start_date = datetime.now()

        user_sub.recurring_payment = True
        user_sub.end_date = end_date
        user_sub.start_date = start_date
        user_sub.active = True
        user_sub.save()

        msg = {'status':'success','message':'request handled successfully' }
        return JsonResponse(status=202,data=msg, safe=False)

    print(response_data)

    msg = {'status':'error','message':'having error with your request' }
    return JsonResponse(status=402,data=msg, safe=False)



@csrf_exempt
@require_POST
@non_atomic_requests
def kyc_notification ( request ):
    try:
        response_data = json.loads(request.body)
        send_mail(
            'Subject here',
            f"{response_data}",
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )
        msg = {'status':'error','message':'you are not authorized to make this push request.' }
        return JsonResponse(status=404,data=msg, safe=False)
    except:
        msg = {'status':'error','message':'you are not authorized to make this push request.' }
        return JsonResponse(status=404,data=msg, safe=False)

    