import pytz

from django.http import JsonResponse
from datetime import datetime
from decimal import Decimal
from django.conf import settings

# import celery
from config import celery_app
from celery.schedules import crontab

from transactions.models import Transactions
from kroon.users.models import User
from payments.models import Payment_Topup

utc=pytz.UTC




# @celery_app.task( name = "topping_up" )
# def topping_fake_token(*args , **kwargs):
#     # getting all pending transactions
#     pending_transactions = Payment_Topup.objects.filter( status='pending' )
#     #checking and verifying if the pin is invalid or expired  
#     current_time = datetime.now()
#     # check_otp_duration = utc.localize(check_otp.duration)
#     current_time = utc.localize(current_time)
#     for i in pending_transactions:
#         if i.pending_duration is not None:
#             if i.pending_duration < current_time:
#                 # updating the transactional table status to cancelled
#                 update_transaction = Transactions.objects.get ( transactional_id = i.payment_ref)
#                 update_transaction.status = 'successful'
#                 update_transaction.save()

#                 """
#                 taking process if the transaction is successful 
#                 processes like toping the user account kroon balance and
#                 also sending email to the user when its been handled 
#                 """

#                 user_token = User.objects.get(id = i.user.id)
#                 # token = TokenRate.objects.get(currency__currency=user_currency)
#                 # token_rate  = int(token.token_rate) * int(amount_paid)
#                 user_token.kroon_token += Decimal(i.amount_in_kroon)
#                 user_token.save()

#                 transactional_history = Transactions.objects.get(transactional_id = i.payment_ref )
#                 transactional_history.kroon_balance = user_token.kroon_token
#                 transactional_history.credited_kroon_amount = Decimal(i.amount_in_kroon)
#                 transactional_history.save()

#                 # updating the payment transaction status
#                 i.settled = True
#                 i.verified = True
#                 i.status = 'successful'
#                 i.save()

#                 return 'this transaction status is updated'

#             else:
#                 return 'this transaction status is on pending'

#         else:
#             return 'this transaction has no pending'

#     return 'transaction is not working'




# celery_app.conf.beat_schedule = {
#     # Execute the cancelling of expired merchants sub every 1 minute
#     'fake-topup-etransac': {
#         'task': 'topping_up',
#         'schedule': crontab(minute='*/1'),
#     },
   
# } 