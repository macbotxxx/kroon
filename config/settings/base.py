"""
Base settings to build other settings files upon.
"""

from pathlib import Path
from datetime import timedelta
import environ

from .apps import * 

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# kroon/
APPS_DIR = BASE_DIR / "kroon"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE")
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG =  False
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "kroon.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "/"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"


# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ROOT_HOSTCONF = 'kroon.hosts'  # Change `mysite` to the name of your project
# DEFAULT_HOST = 'www'  # Name of the default host, we will create it in the next steps

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    # "django_hosts.middleware.HostsRequestMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    # custom middleware
    "gov_panel.middleware.LoggingMiddleware",
    
    # "django_hosts.middleware.HostsResponseMiddleware"
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "kroon.users.context_processors.allauth_settings",
                 # custom context processors
                "kiosk_merchant_dash.context_processors.merchant_business_accounts",
                "gov_panel.context_processors.gov_province",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

OLD_PASSWORD_FIELD_ENABLED  = True
LOGOUT_ON_PASSWORD_CHANGE = True

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Michael Assanama""", "support@mykroonapp.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# https://github.com/celery/celery/pull/6122
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
# CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True
# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_UNIQUE_EMAIL = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "none"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "kroon.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/forms.html
ACCOUNT_FORMS = {"signup": "kroon.users.forms.UserSignupForm"}
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "kroon.users.adapters.SocialAccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/forms.html
SOCIALACCOUNT_FORMS = {"signup": "kroon.users.forms.UserSocialSignupForm"}

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",

    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    # other settings
    # "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",

    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '10/day',
    #     'user': '500/day'
    # },

    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    #     'rest_framework.throttling.ScopedRateThrottle',
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '1000/day',
    #     'user': '1000/day'
    # },
    'DEFAULT_RENDERER_CLASSES': [
        # 'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        # 'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
        # 'core.api.renderers.CustomRenderer',
        # 'rest_framework_json_api.renderers.JSONRenderer',
        # 'rest_framework_json_api.renderers.BrowsableAPIRenderer',
    ],


    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

      
}


REST_AUTH = {
    'LOGIN_SERIALIZER': 'kroon.users.api.serializers.LoginUserSerializer',
    'REGISTER_SERIALIZER': 'kroon.users.api.serializers.SignupSerializer',
    'USER_DETAILS_SERIALIZER': 'kroon.users.api.serializers.UserDetailsSerializer',
    'PASSWORD_CHANGE_SERIALIZER': 'kroon.users.api.serializers.PasswordChangeSerializer',
}

SIMPLE_JWT = {

    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'UPDATE_LAST_LOGIN': True,
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': "cRcpzLRunm5WJt9mRnLySoPdoM2mjFlRcuSOFbB8xOo9kLxW1JQDrT98EjLBQGfh",
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

}


# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
# CORS_URLS_REGEX = r"^/api/.*$"

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGIN_REGEXES = [
r"^https://\w+\.domain\.com$",
]

CORS_ALLOWED_ORIGINS = [
    "https://kroonkioskpro.web.app",
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = (
    "kok-authentication-token",
    "accept-encoding",
    "charset",
    "content-type", 
    "accept", 
    "authorization",
    "bearer",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    )

SWAGGER_SETTINGS = {
    "SUPPORTED_SUBMIT_METHODS": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'destroy',
        'head',
        'delete'
    ],
    'SECURITY_DEFINITIONS': {
        'Api_Key': {
            'type': 'apiKey',
            'description': 'API Keys are issued for specific cases. Contact support for more information.',
            'in': 'header',
            'name': 'KOK-Authentication-Token'
        },
        'Token Authentication': {
            'type': 'apiKey',
            'description': 'If you need to authenticate via bearer auth (e.g., for a cross-origin request), use header `Authorization: Token SMn7BrXSqGmn69mb4GpwRql1Br9KNj` for your API calls. [More info](https://geniopay.docs.apiary.io/#introduction/understanding-authentication)',
            'in': 'header',
            'name': 'Authorization'
        },
        # "OAuth 2.0": {
        #     "type": "oauth2",
        #     'description': 'This API uses OAuth 2 with the implicit grant flow.Idea for application developers. This will enable users to grant your application access to the GenioPay API on their behalf without the need to manually set up or exchange any keys. [More info](https://geniopay.docs.apiary.io/#introduction/understanding-authentication)',
        #     "authorizationUrl": "http://oauth2.geniopay.com/authorize",
        #     "flow": "implicit",
        #     "scopes": {
        #         "write": "allows modifying resources",
        #         "read": "allows reading resources"
        #     }
        # }
    },
    # 'LOGIN_URL': reverse_lazy('account_login'),
    # 'LOGOUT_URL': reverse_lazy('account_logout'),
    'USE_SESSION_AUTH': True,
    'JSON_EDITOR': True,
    'DOC_EXPANSION': 'none',  # ["list"*, "full", "none"]
    'REFETCH_SCHEMA_ON_LOGOUT': True,
    'SHOW_REQUEST_HEADERS': True,
    'APIS_SORTER': 'alpha',
    'DEFAULT_MODEL_DEPTH': 3,  # -1
    'DEFAULT_MODEL_RENDERING': 'example',
    'OPERATIONS_SORTER': 'None',  # [alpha, method, none],
    'TAGS_SORTER': 'alpha',
    'DEEP_LINKING': True,
    'DISPLAY_OPERATION_ID': True,
    'PERSIST_AUTHORIZATION': True,
    # 'SUPPORTED_SUBMIT_METHODS': "[\"get\", \"post\"]",
    'TRY_IT_OUT_ENABLED': True,
    'FILTER': True,
    'WITH_CREDENTIALS': True,
    'PERSIST_AUTHORIZATION': True,
    'DEFAULT_INFO': 'config.admin_api_urls',
    'COMPONENT_SPLIT_REQUEST': True,
    'HIDE_HOSTNAME': False,
    'PATH_IN_MIDDLE': False,
    'REQUIRED_PROPS_FIRST': True
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': True,
    'PATH_IN_MIDDLE': True
}

# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "TITLE": "kroon API",
    "DESCRIPTION": "Documentation of API endpoints of kroon network",
    "VERSION": "2.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
}




# Your stuff...
# ------------------------------------------------------------------------------
TEST_PAYMENT = True

PAYSTACK_SECRET_KEY = env("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = env("PAYSTACK_PUBLIC_KEY")

PAYSTACK_SECRET_KEY_TEST = env("PAYSTACK_SECRET_KEY_TEST")
PAYSTACK_PUBLIC_KEY_TEST = env("PAYSTACK_PUBLIC_KEY_TEST")

FLUTTERWAVE_SECRET_KEY = env("FLUTTERWAVE_SECRET_KEY")
FLUTTERWAVE_PUBLIC_KEY = env("FLUTTERWAVE_PUBLIC_KEY")

FLUTTERWAVE_SECRET_KEY_TEST = env("FLUTTERWAVE_SECRET_KEY_TEST")
FLUTTERWAVE_PUBLIC_KEY_TEST = env("FLUTTERWAVE_PUBLIC_KEY_TEST")

PAYPAL_CID = env("PAYPAL_CID")
PAYPAL_SECRET_ID = env("PAYPAL_SECRET_ID")

USE_ETRANSAC = True

ETRANSAC_PUBLIC_KEY_TEST = env("ETRANSAC_PUBLIC_KEY_TEST")
ETRANSAC_SECRET_KEY_TEST = env("ETRANSAC_SECRET_KEY_TEST")

ETRANSAC_PUBLIC_KEY = env("ETRANSAC_PUBLIC_KEY")
ETRANSAC_SECRET_KEY = env("ETRANSAC_SECRET_KEY")

APPLE_PWD = env("APPLE_PWD")



# PAYPAL KEYS
# live 
# PAYPAL_CLIENT_ID = "AbmFk8h1I12qfgPgMzayLpgZirWNEE3R94UUU00lyOEuKVxMJa_2Ylj5oZ1DhnU49Zoz9YbhCHrVaslu"
# PAYPAL_SECRET_ID = "EHkeh-ShRod8TlDjmEBQwwNYSxVmdTDDe_DEErn43EKl9ypahRdCFYhOd3Pw7QY-bgWCgaQjO59ADxfO"

# test
# PAYPAL_CLIENT_ID = "Acf-VAuyB6NmUCxEPA4u9Y8Ft_TKXFDQqxDunQW4JZ1ae0oDYPZBE597m58zvSUFkEocqBE2PTWxN1xm"
# PAYPAL_SECRET_ID = "EHlwg6Tt7nY5KdJXosLGgiRaiVXY06m4kpASLXBk9cuqiIVrTE5Li-abUZT1H7m0jWrTp-XBk88FI-YD"


# TEST KEYS
# KROON_WEBHOOK_HASH = "KROON_SECK_32379719719yehcjsbcsjc9719-k"

# LIVE KEYS 
KROON_WEBHOOK_HASH = env("KROON_WEBHOOK_HASH")

KOK_AUTH_KEYS = env("KOK_AUTH_KEYS")
KOK_AUTH = False
# wo

FCM_SERVER_KEY = env("FCM_SERVER_KEY")
KIOSK_FCM_SERVER_KEY = env("KIOSK_FCM_SERVER_KEY")
KIOSK_FCM_SERVER_KEY_TAB = env("KIOSK_FCM_SERVER_KEY_TAB")

CURRENCY_CONVERT_API_KEY = env("CURRENCY_CONVERT_API_KEY")

PAYPAL_SANDBOX = False



JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Kroon Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Welcome to Kroon",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Kroon",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "nextonline/logo2.png",

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the kroon admin",

    # Copyright on the footer
    "copyright": "Kroon Library Ltd",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "auth.User",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    # "topmenu_links": [

    #     # Url that gets reversed (Permissions can be added)
    #     {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

    #     # external url that opens in a new window (Permissions can be added)
    #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

    #     # model admin to link to (Permissions checked against model)
    #     {"model": "auth.User"},

    #     # App with dropdown menu to all its models pages (Permissions checked against models)
    #     {"app": "books"},
    # ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    # "usermenu_links": [
    #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    #     {"model": "auth.user"}
    # ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages", 
            "url": "make_messages", 
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": True,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-primary navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "materia",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": False
}



