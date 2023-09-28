from django.urls import path, re_path
from . import views





urlpatterns = [

    path('', views.index, name = 'gov_panel_home'),

    # users onboarding
    # start here
    path('onboarding/', views.gov_users_on_boarding, name = 'gov_users_on_boarding'),
    path('users-list/', views.gov_users_list, name = 'gov_users_list'),
    path('onbaording-progress/', views.gov_onboarding_progess, name = 'gov_onboarding_progess'),
    path('gov-users-details/<str:id>/', views.gov_users_details, name = 'gov_users_details'),
    # end here
    # users onboarding

    # users push notification
    # start here
    path('push-notifications/', views.gov_push_notification, name = 'gov_push_notification'),
    path('publish-feeds/', views.gov_publish_notification, name = 'gov_publish_notification'),
    path('edit-newsfeed/<str:id>/', views.gov_edit_newsfeed, name = 'gov_edit_newsfeed'),
    path('approve-newsfeed/<str:id>/', views.gov_newsfeed_approval, name = 'gov_newsfeed_approval'),
    path('delete-newsfeed/<str:id>/', views.gov_newsfeed_delete, name = 'gov_newsfeed_delete'),
    path('push-ads/', views.gov_push_ads, name = 'gov_push_ads'),
    path('push-ads-list/', views.gov_push_ads_list, name = 'gov_push_ads_list'),
    # users push notification
    # start here

    # merchants stores and province url paths 
    path('store-list/', views.gov_store_list, name = 'gov_store_list'),
    path('store-details/<str:id>/', views.gov_store_details, name = 'gov_store_details'),
    path('store-by-province/<str:id>/', views.store_by_province, name = 'store_by_province'),
    path('merchants-by-province/<str:id>/', views.users_by_province, name = 'users_by_province'),
    # merchants stores endhere

    # store details records
    path('store-revenue/<str:id>/', views.store_revenue, name = 'store_revenue'),
    path('store-products/<str:id>/', views.store_products_list, name = 'store_products_list'),
    path('store-workers/<str:id>/', views.store_workers, name = 'store_workers'),
    # store details records
    

    # gov worker
    path('verify-gov-worker/', views.verify_gov_worker, name = 'verify_gov_worker'),
    path('gov-workers/', views.gov_workers, name = 'gov_workers'),
    path('remove-gov-workers/<str:email>/', views.gov_remove_workers, name = 'gov_remove_workers'),
    path('register-gov-workers/', views.gov_register_worker, name = 'gov_register_worker'),
    path('verify-gov-workers-otp/', views.verify_gov_worker_opt, name = 'verify_gov_worker_opt'),
    path('add-gov-workers-otp/', views.gov_add_workers, name = 'gov_add_workers'),
    # gov worker endhere

    # action and broswers logs 
    path('broswer-logs/', views.broswer_logs, name = 'broswer_logs'),
    path('action-logs/', views.gov_actions_logs, name = 'gov_actions_logs'),
    path('gov-account-settings/', views.gov_account_settings, name = 'gov_account_settings'),
    # action and broswers logs endhere 


    re_path(r'^user-test/', views.onboarding_process, name = 'onboarding_process'),
    path('merchant-report/', views.gov_merchant_report, name = 'gov_merchant_report'),
    path('province-report/<str:id>/', views.gov_province_report, name = 'gov_province_report'),
    path('national-report/', views.pdf, name = 'national_report'),

    # NASME users
    path('nasme-users-list/<str:id>/', views.nasme_users, name = 'nasme_users_list'),




]