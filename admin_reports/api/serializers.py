from rest_framework import serializers
from kroon.users.models import User
from transactions.models import Transactions, KroonTokenTransfer , KroonTokenRequest, UserRequestToken
from admin_reports.models import AdminPushNotifications
from django.utils.translation import gettext_lazy as _
from admin_reports.choices import ModelChoices
from locations.api.serializers import CountryDetails
from kroon.users.api.serializers import UserOnlyInfo
from e_learning.models import Kiosk_E_Learning, AppSurveyQuestion , SurveyQA , App_Survey

class UserListSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name','wallet_id','email','gender','created_date','modified_date',]


class TransactionsListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = [
            'transactional_id',
            'amount',
            'currency',
            'amount_in_localcurrency', 
            'local_currency',
            'action',
            'status',
            'created_date',
            'modified_date',
            ]
        


class TransactionDetailsSerializers(serializers.ModelSerializer):
    benefactor = UserListSerializers( read_only=True )
    recipient = UserListSerializers( read_only=True )
    class Meta:
        model = Transactions
        fields = [
            'transactional_id',
            'amount',
            'currency',
            'amount_in_localcurrency', 
            'local_currency',
            'action',
            'status',
            'created_date',
            'modified_date',
            ]
        read_only_fields = ['benefactor', 'recipient', 'transactional_id', 'flw_ref', 'amount', 'amount_in_localcurrency', 'currency', 'local_currency', 'amount_settled', 'debited_kroon_amount', 'credited_kroon_amount', 'kroon_balance', 'payment_type', 'narration', 'device_fingerprint', 'transactional_date', 'ip_address', 'card', 'card_first_6digits', 'card_last_4digits', 'card_issuer', 'card_country', 'card_type', 'card_expiry', 'billing_id', 'billing_name', 'billing_mobile_number', 'billing_email', 'billing_date', 'service_providers', 'action', 'status',]



class AdminPushNotificationsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=150,
        help_text=_("The notification title that will be displayed to the user mobile device.")
    )

    body_message = serializers.CharField(
        max_length=200,
        help_text=_("this holds the content of the push notification")
    )

    platform = serializers.ChoiceField(
        choices=ModelChoices.APP_TYPES,
        default= ModelChoices.APP_TYPE_ALL,
        help_text=_("This holds the platform that is only valid to recieve the push notification, which can also be identified as the 'all the above' which shows the contents for devices and platforms that is registered under kroon network.")
    )

    class Meta:
        model = AdminPushNotifications
        fields = "__all__"
        read_only_fields = ['id','publisher','notification_type','status','created_date','device_type',]

    # def validate_title(self, value):
    #     if budget_exist := self.Meta.model.objects.filter(title__iexact=value).exists():
    #         self.register_error(
    #             error_message="A budget already exists with this name.",
    #             error_code="name_already_exist",
    #             field_name="name"
    #         )
    #     return value

    # def create(self, validated_data):
    #     return super().create(validated_data)


class NotificationInfo(serializers.ModelSerializer):
    publisher = UserOnlyInfo( read_only = True)
    news_feed_country = CountryDetails( read_only = True , many = True )
    class Meta:
        model = AdminPushNotifications
        fields = "__all__"


class ELearningSerializers(serializers.ModelSerializer):
    class Meta:
        model = Kiosk_E_Learning
        fields = "__all__"
        read_only_fields = ['id','created_date',]

class ElearningInfo(serializers.ModelSerializer):
    e_leanring_country = CountryDetails( read_only = True , many = True )
    class Meta:
        model = Kiosk_E_Learning
        fields = "__all__"
        read_only_fields = ['id','created_date',]


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSurveyQuestion
        fields = "__all__"
        read_only_fields = ['id','created_date',]


class SurveyQuestioninfo(serializers.ModelSerializer):
    survey_questions_id = SurveyQuestionSerializer( read_only=True)
    class Meta:
        model = SurveyQA
        exclude = ['survey_qa']
        read_only_fields = ['id','created_date',]

class SurveyUsers(serializers.ModelSerializer):
    class Meta:
        model = App_Survey
        fields = ["id",]
        read_only_fields = ['created_date',]
