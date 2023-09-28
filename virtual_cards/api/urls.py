from django.urls import path
from . import views

urlpatterns = [
    
    path('virtual-cards/' , views.Create_Virtual_Cards_View.as_view(), name='virtual-cards'),
    path('virtual-cards/<str:card_id>/' , views.Virtual_Cards_Details_View.as_view(), name='virtual-cards-details'),
    path('virtual-cards/<str:card_id>/fund/' , views.Fund_Card_view.as_view(), name='fund-virtual-cards'),
    path('virtual-cards/<str:card_id>/status/<str:status_action>/' , views.Block_Virtual_Card.as_view(), name='block-virtual-cards'),
    path('virtual-cards/<str:card_id>/terminate/' , views.Terminate_Virtual_Card.as_view(), name='terminate-virtual-cards'),
    path('virtual-cards/<str:card_id>/transactions' , views.Card_Transaction.as_view(), name='virtual-cards-transactions'),
    path('initiate-payment/', views.Initiate_Payment.as_view(), name='initiate-payment'),

]