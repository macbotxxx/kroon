
# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "jazzmin", 
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'drf_yasg',
    "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_celery_beat",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    # "drf_spectacular",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "ckeditor",
    "tinymce",
    "corsheaders",
    "import_export",
    "helpers",
    "locations",
    "mptt",
    "django_filters",
    # "drf_standardized_errors",
    # "django_hosts",
]

LOCAL_APPS = [
    # the admin reports app 
    "admin_reports.apps.AdminReportsConfig",
    
    "kroon.users",
    # Your stuff: custom apps go here
    "accounts.apps.AccountsConfig",
    "transactions.apps.TransactionsConfig",
    "kroon_kyc.apps.KroonKycConfig",
    "kroon_token.apps.KroonTokenConfig",
    "ads.apps.AdsConfig",
    "kroon_kiosk.apps.KroonKioskConfig",
    "mobile_money.apps.MobileMoneyConfig",
    "webhooks.apps.WebhooksConfig",
    "kroon_otp.apps.KroonOtpConfig",
    "kroon_gift.apps.KroonGiftConfig",
    "notifications.apps.NotificationsConfig",
    "statement_of_account.apps.StatementOfAccountConfig",
    "generate_pin.apps.GeneratePinConfig",
    "kroon_withdrawal",
    # "withdrawal_queue",
    "working_tasks",
    "payments.apps.PaymentsConfig",
    "subscriptions.apps.SubscriptionsConfig",
    "promotional_codes.apps.PromotionalCodesConfig",
    "virtual_cards.apps.VirtualCardsConfig",
    "kiosk_agreements.apps.KioskAgreementsConfig",

    # sandbox IBAN Application
    # "iban_sandbox.apps.IbanSandboxConfig",
      
]


KIOSK_APPS = [
    
    # Here goes the kiosk apps 
    "kiosk_categories.apps.KioskCategoriesConfig",
    "kiosk_stores.apps.KioskStoresConfig",
    "kiosk_cart.apps.KioskCartConfig",
    "kiosk_sales_report.apps.KioskSalesReportConfig",
    "kiosk_worker.apps.KioskWorkerConfig",
    "kiosk_business_plan.apps.KioskBusinessPlanConfig",
    "e_learning.apps.ELearningConfig",
    "kiosk_offline_mode.apps.KioskOfflineModeConfig",
    "kiosk_logs.apps.KioskLogsConfig",
    # "kiosk_subscribers.apps.KioskSubscribersConfig",
    "simulation.apps.SimulationConfig",
    
]


GOV_PANEL = [
    "gov_panel.apps.GovPanelConfig",
    "training_cert.apps.TrainingCertConfig",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + KIOSK_APPS + GOV_PANEL
