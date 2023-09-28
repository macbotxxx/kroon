from django.urls import path
from . import views

urlpatterns = [
    path('all-transactions/', views.TransactionView.as_view(), name='all-transactions'),
    
    path('get-wallet-id/<str:wallet_id>/', views.WalletIDView.as_view(), name='wallet_id'),

    path('credit-transactions/', views.CreditTransactionDetails.as_view(), name='credit-transactions'),
    path('debit-transactions/', views.DebitTransactionDetails.as_view(), name='debit-transactions'),
    
    # path('convert-token/<str:amount>/<str:currency>/', views.TokenConvert.as_view(), name='tokenconvert'),
    path('transfer-token/', views.TokenTransfer.as_view(), name='transfer_token'),
    path('token-request/', views.Open_TokenRequest.as_view(), name='token'),
    path('token-request-payment/', views.Open_TokenRequest_Payment.as_view(),name='token_payment'),

   
    path('create-transaction-pin/', views.TransactionPin.as_view(), name='create_transaction_pin'),
    path('sms/', views.PushNotification.as_view(), name='sms'),
    path('change-transactional-pin/', views.ChangeTransactionPin.as_view(), name='update_transactional_pin'),
    path('customer-kroon-request/', views.UserKroonRequestView.as_view(), name='customer-requst'),
    path('decline-customer-kroon-request/', views.DeclineTokenRequest.as_view(), name='decline-customer-request'),
    path('accept-customer-kroon-request/', views.AcceptTokenRequest.as_view(), name='accept-customer-request'),
    path('statement-of-account/', views.StatementOfAccountView.as_view(), name='state-of-account'),

    path('fast-checkout/', views.FastCheckout.as_view(), name='fast-checkout'),
    path('fast-checkout-payment/', views.FastCheckoutPayment.as_view(),name='fast-checkout-payment'),
    path('cancel-fast-checkout-payment/', views.CancelFastCheckoutRequest.as_view(),name='fast-cancel-payment'),

    path('verify-pin/', views.Verify_Transactionan_Pin_View.as_view(), name='verify-pin'),

]
