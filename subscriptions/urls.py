from django.urls import path

from . import views

urlpatterns = [

    path('plans/', views.all_plans, name='all_plans'),
    path('plan-details/<str:plan_id>/<str:period>/', views.plans_details, name='plans_details'),
    path('government-promo-code/<str:plan_id>/', views.government_code, name='government_code'),
    path('my-subscriptions/', views.my_subscriptions, name='my_subscriptions'),
    path('generate/', views.generate_code, name='generate_code'),
    path('migrate-plan-verify/<str:plan_id>/<str:period>/', views.card_subscription, name='card_subscription'),
    path('paypal-payment/', views.PayPal_Payment, name='PayPal_Payment'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('app-sub-page/', views.inapp_sub_page, name='inapp_sub_page'),

    # mobile app subscriptions
    path('app-plans/<str:email>/', views.all_app_sub, name='all_app_sub'),
    path('app-details/<str:plan_id>/<str:period>/', views.app_plan_details, name='app_plan_details'),
    path('inapp-government-promo-code/<str:plan_id>/', views.in_app_government_code, name='in_app_government_code'),


]