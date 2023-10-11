from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from drf_yasg.utils import swagger_auto_schema

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from kroon.users.api.views import MyTokenObtainPairView , KroonKioskTokenView

schema_view = get_schema_view(
   openapi.Info(
      title="Kroon API V2",
      default_version='v1',

      description="""
            Kroon Network is the new wave of International Money transfer in over 30
            currencies. The landscape of Kroon Network is to redefine how money is moved
            across the globe. With cutting edge technology, we offer users with
            Borderless accounts and settlement accounts in about 38 trading currencies.


            Our REST API permits applications to connect securely to the Kroon Network
            software to carry out a multitude of operations. Depending on the operations
            in question, authentication and token-based access control is enforced.


            ## API Overview


            To interact with your Kroon Network system via the Kroon Network API you need to send
            requests to the backend (API) URL. For white label solutions, this base URL
            can be determined by appending "api/v1' to your Kroon Network system's URL. If
            your system is hosted at https://username.example.com then the base API URL
            will be https://username.example.com/api/v1.


            The documentation that follows is intended for developers, providing an
            introduction to using the API and additionally describing all currently
            available endpoints. We recommend you read the documentation to familarise
            yourself with conventions, parameters and response structure.


            A dedicated sandbox for testing purposes can be made available to users upon
            request.

            This document explains how to integrate with Kroon Network API to process and
            analyse account information.                 &nbsp;


            All responses will be shown in JSON format.
                    &nbsp;

            If you wish to consume our API using Oauth2, make sure you have acquired an
            API Client ID and Client Secret from the Kroon Network Developer Dashboard.


            **For Kroon Network Partners**: In your Partner dashboard, you will see a
            personalized link that reveals additional API endpoints allowed for
            Partners.

            ## Project Information

            URLs and functionality differs if you use a specific implementation of
            Kroon Network APIs at your company, educational institution or during an event.
            You will be provided with additional information that helps you to do the
            translation of e.g.


            ## Develop and Debug

            ### Sandbox ###

            The Kroon Network is based on a sandboxed version of our industry leading banking solution
            Kroon Network. It comes with thousands of function and features. "Sandboxed" means it is not
            connected to any external systems, so some functions may not work as expected or not at all,
            in particular those that rely on external connections (e.g. SEPA transfers).


            The sandbox environment provides a true replica of the production system without making
            any real money transfers. Transfers can still be made, but they will send fictional money
            to fictional recipients only.

            If API credentials have been provided, the sandbox environment should be used instead of
            the mock.

            ### Production ##

            The production environment should be targeted by production systems only. Any transfers made on production will send real money to real recipients. Special care must be taken to ensure the production API cannot be accessed by unauthorised personnel or test systems, otherwise it may have irreversible consequences.

            ### User account types ###

            The sandbox knows two different kind of user accounts:

            * developer accounts (that is you)

            * customer accounts (accounts to play with)

            You can register for a developer account by yourself. Customer accounts and respective
            credentials (login and password) will be provided to you by your teacher or your account
            manager.

            ### Digital Wallets ###

            Sandbox customer accounts have a related bank account including a small amount of (simulated)
            money to start with. Developer accounts do not have a bank account. Right now only
            retail current accounts are created.


            In order to access and manipulate a bank account you have to provide the respective
            account holder's customer account credentials (more precisely: an OAuth2 token
            created using the account holders credentials). Simulations are categorically done by making API
            calls to respective endpoints.

            ## Idempotent Request

            Idempotency ensures that an API request completes no more than one time. With an
            idempotent request, if the original request completes successfully, all subsequent
            retries return the result from the original successful request and they have no
            additional effect.


            To perform an idempotent request, provide an additional `Idempotency-Key`: <key>
            header to the request.


            The idempotency key should be an unique value generated by the client which the
            server uses to recognize subsequent retries of the same request. We suggest using
            V4 UUIDs, or another random string with enough entropy to avoid collisions.


            `Idempotency-Key` should only be sent in POST messages. A successful POST message
            will return HTTP code 201. A successful POST message with a previous
            processed `Idempotency-Key` will return HTTP code 200 with a copy of the
            original POST result.


            Idempotency-Keys are valid for 3600 seconds

            ## Understanding Authentication

            ### What is OAuth? ###

            OAuth is an open standard for access delegation, commonly used as a way for Internet users to grant websites or applications access to their information on other websites but without giving them the passwords. – Whitson Gordon


            The Kroon Network API offers many functions to retrieve information from your and other
            people's bank accounts, community accounts, and much more. The extent of access that
            your application needs is configured when you define the scope of your application in
            the Application Manager.

            In order to actually access the account and retrieve the requested data, the account
            holder must authorize your application and allow it to access his/her account. This
            is achieved using OAuth 2.

            ### Client-facing Apps vs. Server-side Connection ###

            Kroon Network customers have diverse use cases for the Kroon Network API, ranging from payment
            automation without any user interaction to situations where consumers will sit in
            front of the computer every time they use the application. Applications run on PCs,
            on mobile devices, on premise service, and in the cloud. All this has implications
            on time and means of authentication and authorization.

            ### Web Server Flow and Alternatives ###

            This following documentation focusses on the interactive 3-legged Authorization
            Code (or Web Server) Flow to obtain the access_token and refresh_token. That is
            particularly useful for server-based, client-facing web apps and supports 3rd-party
            application providers.

            For pure server-to-server based applications we offer alternatives, e.g. static
            tokens (that we create for you), please talk to our customer service. It is worth
            mentioning that even in server only settings you can bootstrap the token process
            by going through an interactive session once and work with refresh_tokens from there on.

            ### Account Holder Perspective ###

            From the account holder's perspective, the process works as follows:

            * the account holder using your application is redirected to Kroon Network.
            In case they are not already logged in, they are asked
            to **enter username and password**

            * in case the account holder has not previously authorized your app, the user
            is displayed the list of permissions your application is requesting and
            is **asked to confirm that the app is allowed to access their account with the
            given scope**.

            Afterwards, the account holder is returned to your app, which will make calls
            to the API and display the results.

            ### Application Perspective ###

            From the perspective of your application, the OAuth2 process consists of three steps:

            * You point the **account holder's browser** to the Authorization Endpoint.

            * This endpoint returns an **Authorization Code** if the account holder
            was successfully authenticated and authorized the scope of the app.

            * You retrieve the **OAuth bearer token** (aka. access-token) by sending
            your app's Client Credentials along with the Authorization Code to the Token Endpoint.

            If the account holder declines your request somewhere in the process we
            try to redirect to your `redirect_uri` and add **?error=user_denied** to the URL.

            ## Direct Debit Information

            ### Introduction ###

            Before collecting payments from your customer by Direct Debit, your customer must issue you with a mandate. This mandate - officially called a "Direct Debit Instruction" (DDI) or more commonly referred to as a "Direct Debit Mandate" - authorises you to collect future payments from your customer.

            Although the details slightly differ per payment scheme, a Direct Debit Mandate generally comprises:

            * Authorisation to collect all future payments from your customer​​ independent of amount, time or frequency

            * Liability to notify your customer of each payment before it is collected.

            * Protection of your customer from payments taken in error.

            To create a Direct Debit Mandate your customer must complete a DDI form. This can be generally done in three ways:

            - Online Mandate - You collect the customers details online using bank approved web pages. Online Mandates are commonly further differentiated by the way your customer approves the mandate:

                - Click Mandate - Your customer approves the mandate by ticking a check box and/or clicking an approve button on the web page.
                - Email Mandate - Your customer is sent an email as part of the checkout process containing a secret PIN and/or a link to click. By typing the secret PIN into the web page or by clicking on the link your customer approves the mandate.
                - SMS Mandate - Your customer is sent a SMS text message as part of the checkout process containing a secret PIN. By typing the secret PIN into the web page your customer approves the mandate.
                - AIS Mandate - Your customer approves the mandate by login to customers bank account.

            - Paper Mandate - You collect the customers details by handing out a printed form which the customer completes and returns to you. The layout and content of paper DDI forms are strictly controlled by the Direct Debit rules of the used payment scheme and the form you are using has to be approved by your bank before usage. Returned paper DDI forms should be retained as proof your customer has authorised a payment.

            - Telephone Mandate - You collect the customers details by calling your customer over the telephone using a bank approved script.

            Some payment schemes require the details of an approved Direct Debit Mandate to be submitted electronically to the bank of the customer. Mandates for such payment schemes have to be managed by Kroon Network.


            All other mandates can be managed either by the Merchant, the PSP or optionally by Kroon Network. It is important to note that independently of who manages a mandate always a mandate entity has to be created inside Kroon Network.

            Please note that determined by multiple factors, like the used payment scheme, your verticals or the bank in charge of your account, not every option might be available.

            ## Standards

            ### ISO Codes ###

            Our API makes use of the following ISO Codes defined by the International Organization for Standardization (ISO):

            - Country Codes: [ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements) alpha-2 codes, e.g. CH for Switzerland

            - Currency Codes: [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) e.g. EUR for Euro

            - Times and Dates: [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)

            ### Other Standards ###

            Our API also makes use of other recommendations.

            - Mobile numbers follow the [E.164 Recommendation](https://en.wikipedia.org/wiki/E.164).
            The number should be starting with a + followed by 7 to 15 digits.
            Whitespace and any of /_- will be stripped from the string before validation.

            - SEPA transaction data is verified against
            [EPC217-08](http://www.europeanpaymentscouncil.eu/index.cfm/knowledge-bank/epc-documents/sepa-requirements-for-an-extended-character-set-unicode-subset-best-practices/epc2017-08-best-practices-sepa-requirements-for-an-extended-character-set/).
            We documented this in the section above.

            - Paged results are in line with [RFC5988](https://tools.ietf.org/html/rfc5988) in that
            link relations are yielded in the header of responses.
            See  [Pagination and Filtering](ref:pagination-and-filtering-1)  for further details.

            - Return codes for SEPA follow general EPC guidance on reason codes for R-transactions,
            e.g. [EPC173-14](https://www.europeanpaymentscouncil.eu/document-library/guidance-documents/epc-guidance-reason-codes-sepa-direct-debit-r-transactions)


            ### SEPA Characters ###

            The EPC proposed a best practice digest, EPC217-08, which limits the allowed characters
            in SEPA transactions in order to maintain conclusive processing in computerized environments.

            This character set is currently enforced on the following fields:

            - SEPA direct debit

            - `end_to_end_id`

            - `description`

            - within mandate the fields
            - `reference`
            - `debtor_name`

            - SEPA credit transfer

            - `recipient_name`

            - `end_to_end_id`

            - description

            The digest makes use of a restricted basic latin alphabet, which results in the following
            characters being accepted:

            - Upper case letters: `A B C D E F G H I J K L M N O P Q R S T U V W X Y Z`

            - Lower case letters: `a b c d e f g h i j k l m n o p q r s t u v w x y z`

            - Numbers: `0 1 2 3 4 5 6 7 8 9`

            - Special characters: `/ - ? : ( ) . , ' +`

            - With the exception of `mandate`/`reference` and `end_to_end_id`, all fields may contain
            spaces (but no leading spaces)

            In addition, the following applies to the structure of text fields:

            - The string must not contain two or more consecutive slashes (/) anywhere in the text.

            - The string must not start and/or end with a slash (/)

            Data exchange in the context of SEPA requires us to escape specific characters with a
            dedicated representation. In this event, the length of this representation is taken
            into consideration when checking the length of the string — in other words, one
            character is counted as multiple characters. Your own string length checks should
            take this into account.

            ### Merchant Category Codes ###

            Our API makes use of the MCCs referred to in the [Visa Merchant Data Standards Manual](https://usa.visa.com/content/dam/VCOM/download/merchants/visa-merchant-data-standards-manual.pdf) which contains requirements for merchant/payment, facilitator/marketplace classification, location, and various data elements, including merchant location, merchant category codes (MCC), and other VisaNet data formats.
            You can also retrieve a list of Merchant Category Codes by calling the List Merchant Category Code endpoint.

            ## Pagination and Filtering

            We offer pagination through URL parameters. Pagination allows you to break down lists into
            pages when fetching them via `GET` request, which speeds up loading time and enables
            processing in batches.

            Not all available data is dumped at once. With pagination and filtering, you can control
            the output and navigate through these pages.

            The options to control pagination are:

            - page[number]

            - page[size], defaults to 10, maximum is 100


            The page index (page[number]) only accepts positive integers and defaults to 1 otherwise.

            Some endpoints, especially the ones expected to hold many entries, are configured to
            include special pagination headers defined in the web linking standard (RFC5988).
            Their response headers contain a total count of expected entries under the total field
            and the current page[size] value in the per-page field for confirmation (with fallback
            to the maximum size specified above). Page numbers which go beyond the number of
            objects simply return an empty array.


            The example in the right-hand column requests page number two with a batch size of 15,
            resulting in the objects 16 through 30. The response shows fields specific to the
            web linking standard.


            ## Link Attribute

            The example response in the right-hand column makes use of an additional header
            attribute called `link`. Although the specification lists a wide range of uses for
            this field, we limit ourselves to links only for the `first`, `last`, `prev` (previous)
            and `next` pages in the resource. `prev` and `next` are respectively omitted with the
            first and last page of the resource.


            Each link in this comma-separated list is followed by an optional link parameter, of which
            we currently only use `rel` to indicate relations between pages within the resource.
            URI in this list are generally URL encoded, i.e. special characters like brackets ([])
            or spaces are escaped to their equivalent percent-literal notation.


                {api_url}/transactions/?sort=created_date&page[size]=2&page[number]=20&filter[search]=XHCH210A44


            Different endpoints provide different sets of filters so please see the respective
            endpoint documentation for details on that.


            ### Collections ###

            Most data you get from the API will have a supplementary collection object to provide
            information about the pagination and indicate your current place in a collection.


                "meta": {
                    "pagination": {
                    "page": 1,
                    "pages": 10,
                    "count": 100
                    }
                },
                "links": {
                    "first": "http://example.com/?page_number=1",
                    "last": "http://example.com/?page_number=10",
                    "next": "http://example.com/?page_number=2",
                    "prev": null
                    }

            ### Sorting ###

            Similar to pagination the API also offers sorting through URL query parameters on `GET`
            requests. The sorting is based on the fields of that resource.

            The list below shows what sorting options each resource contains.

            The name of the field as value of the sorting GET parameter enforces ascending sorting
            (e.g. `created_date`), minus sign in front of the field name enforces descending sorting (e.g. `-created_date`).

            For 'transactions', the following fields are available for sorting:

            - `created_date`

            - `booking_date`

            - `completed_date`


            ## Integrations

            Kroon Network offers two ways to integrate its services into a PSP. Both with its own
            advantages and disadvantages.

            ### Backend (S2S) Integration ###

            In this setup the backend of the PSP, and only the PSP, is calling the Kroon Network
            REST API endpoints.


            Advantages:

            * Pure backend integration at the PSP

            * No integration in the frontend

            * No integration at the merchant

            * Full white label solution


            Disadvantages:

            * Merchant or PSP have to implement and constantly update all the frontend logic,
            workflows and regulatory requirements of the used payment schemes.

            * Greater complexity in the PSP backend

            ### Hosted Payment Pages ###

            In this setup the merchant or PSP is integrating the hosted payment pages provided by
            Kroon Network.

            Advantages:

            * Easy to setup

            * Reduced complexity in the PSP backend

            * Always up-to-date with all regulatory requirements

            Disadvantages:

            * No full white label support possible

            * Intrusive into the frontend

            * Less control of the payment process

            ## How to Use Sandbox

            The [Kroon Network](https://mykroonapp.com) is a limited version of production
            console. Consider our Sandbox as a Graphical User representation of the API calls.
            Limited task can be performed directly in the Sandbox. For example, creating a new account,
            change user password and other transactional task - Open a Borderless Wallet, Make a Pay-In and Pay-Out etc.


            Any other API operations should be directly executed by calling the specified endpoint.


            For example to perform a Balance Transfer or Balance Exchange, Add a new Beneficiary template, create a Money Jar etc.
            After successfully executing an endpoint, you can then check the corresponding record in your Sandbox account.

        """,

      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@kroonapp.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path('auth/api/v1/', include('dj_rest_auth.urls')),
    path('auth/api/v1/create-account/', include('dj_rest_auth.registration.urls')),
    re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
    # User management
    # path("users/", include("kroon.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),

    # API base url
    # path("users/", include("kroon.users.urls", namespace="users")),
    path("task/", include("withdrawal_queue.urls")),
    path("test/", include("testing.urls")),
    path('tinymce/', include('tinymce.urls')),
    path('subscriptions/', include('subscriptions.urls')),

    path('documentation/json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
   
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# API URLS
urlpatterns += [
    # API base url
    # path('admin-reports/api/v1/', include('admin_reports.api.urls')),
    # path("api/v1.0/", include("config.api_router")),
    path("api/v1.0/", include("admin_reports.api_router")),
  
    # DRF auth token and registration
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/kroon-kiosk-token/', KroonKioskTokenView.as_view(), name='kroon_kiosk_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('auth/api/v1/create-account/', include('rest_auth.registration.urls')),
    # path('auth/api/v1/', include('rest_auth.urls')),
    path('webhook/', include('webhooks.urls')),
    path('statment-of-account/', include('statement_of_account.urls')),
    # path('api/v1/accounts/confirm-email/<str:key>',confirm_email, name='account_confirm_email'),

    # kroon app 
    path('locations/api/v1/', include('locations.api.urls')),
    path('kroon-kyc/api/v1/', include('kroon_kyc.api.urls')),
    path('kroon-user/api/v1/', include('kroon.users.api.urls')),
    path('withdrawal/api/v1/', include('kroon_withdrawal.api.urls')),


    path('business-plan/api/v1/', include('kiosk_business_plan.api.urls')),
    path('mobile-money/api/v1/', include('mobile_money.api.urls')),
    path('ads/api/v1/', include('ads.api.urls')),
    path('fees-vet/api/v1/', include('kroon_token.api.urls')),
    path('kroon-opt/api/v1/', include('kroon_otp.api.urls')),
    path('gift-kroon/api/v1/', include('kroon_gift.api.urls')),
    path('notifications/api/v1/', include('notifications.api.urls')),
    path('generate-pin/api/v1/', include('generate_pin.api.urls')),
    path('payments/api/v1/', include('payments.api.urls')),
    path('bank-information/api/v1/', include('bank_information.api.urls')),
    path('subscription/api/v1/', include('subscriptions.api.urls')),
    path('transactions/api/v1/', include('transactions.api.urls')),
    path('agreements/api/v1/', include('kiosk_agreements.api.urls')),
    path('gov-panel/api/v1/', include('gov_panel.api.urls')),

    # e-leanring 
    path('e-learning/api/v1/', include('e_learning.api.urls')),

    # virtual cards 
    path('virtual-cards/api/v1/', include('virtual_cards.api.urls'),name="instances"),

]

# WORKERS URL INDEX 

urlpatterns += [
    path('marketers/', include('marketers.urls')),
    path('financial/', include('financial.urls')),
]

# KIOSK URLS 
urlpatterns += [
    # KIOSK BASE URL

    path('kiosk-categories/api/v1/', include('kiosk_categories.api.urls')),
    path('kiosk-products/api/v1/', include('kiosk_stores.api.urls')),
    path('kiosk-cart/api/v1/', include('kiosk_cart.api.urls')),
    path('kiosk-sales/api/v1/', include('kiosk_sales_report.api.urls')),
    path('kiosk-workers/api/v1/', include('kiosk_worker.api.urls')),
    path('kiosk-offline-mode/api/v1/', include('kiosk_offline_mode.api.urls')),
    # path('financial/', include('financial.urls')),
    # IBAN SANDBOX

    # path('iban-sandbox/api/v1/', include('iban_sandbox.api.urls')),

]


urlpatterns += [
    # MERCHANT WEB DASHBOARD
    path('', include('kiosk_merchant_dash.urls')),
    path('kiosk/', include('kiosk_worker.urls')),
    path('kiosk/', include('kiosk_business_plan.urls')),
]

urlpatterns += [
    # Gov Panel WEB DASHBOARD
    path('gov-panel/', include('gov_panel.urls')),
    path('training-cert/', include('training_cert.urls')),
    path('simulate/', include('simulation.api.urls')),
]




if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns