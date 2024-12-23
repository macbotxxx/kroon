import contextlib

from django.http.response import Http404
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters
from django.db.models import Sum, Count
from datetime import date, timedelta

from kroon.users.pagination import StandardResultsSetPagination
from helpers.common.security import KOKPermission
from kroon.users.models import User
from admin_reports.models import AdminNewsFeed
from admin_reports.task import device_push_notification
from admin_reports.permissions import IsBlekieAndEtransac
from e_learning.models import Kiosk_E_Learning , App_Survey, SurveyQA , AppSurveyQuestion
from ads.models import Ads
from locations.models import Country
from kroon.users.models import User, BusinessProfile
from kroon.users.api.serializers import BusinessProfileSerilizer
from locations.models import Country , Country_Province
from kiosk_stores.models import Merchant_Product
from kiosk_cart.models import Order,OrderProduct , Payment





from transactions.models import (
    Transactions, 
    KroonTokenTransfer, 
    KroonTokenRequest, 
    UserRequestToken
    )
from kroon.users.api.serializers import UserDetailsSerializer
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet
from .serializers import (
    UserListSerializers,TransactionsListSerializers , 
    TransactionDetailsSerializers,AdminNewsFeedSerializer,
    NotificationInfo,ELearningSerializers,
    ElearningInfo,SurveyQuestionSerializer,
    SurveyUsers,SurveyQuestioninfo,
    AdsSerializer,AdsInfo,
    AdminRecordFilter

    )





class AllUserListView(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
    ):
    """
    Get all Users 

    This endpoint allows you to get all users registered in kroon and kiosk
    """
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "wallet_id"
    serializer_class = UserListSerializers
    queryset = User.objects.select_related('country_of_residence','country_province','on_boarding_user', 'government_organization_name','bank_details').filter(Q(country_of_residence__iso2 = "NG" ) | Q(country_of_residence__iso2 = "GH") ) #getting the full list of Nigerians and ghana users
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['created_date', 'modified_date']
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

    def get_object(self, queryset=None):
        return User.objects.filter(wallet_id=self.kwargs["wallet_id"]).first()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="All User",
        operation_description="Endpoints retrieves the list of registered users both on kroon and kiosk.",
    )
    def list(self, request, *args, **kwargs):
        return super(AllUserListView, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get A User",
        operation_description="Retrieve the information of a user by passed Wallet Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            # any additional logic
            serializer = UserDetailsSerializer(instance)

            return Response(serializer.data)



class TransactionListView(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
    ):
    """
    Get all transactions 

    This endpoint allows you to get all transactions been made by the users in kroon and kiosk

    A transaction details consists of the following TOPUP, KROON TRANSFER , WITHDRAWAL

    """
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "transactional_id"
    serializer_class = TransactionsListSerializers
    queryset = Transactions.objects.all()
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['created_date', 'modified_date']
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

    def get_object(self, queryset=None):
        return Transactions.objects.filter(transactional_id=self.kwargs["transactional_id"]).first()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="All Transactions",
        operation_description="Endpoints retrieves the list of Transactions.",
    )
    def list(self, request, *args, **kwargs):
        return super(TransactionListView, self).list(request, *args, **kwargs)


    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get Transaction",
        operation_description="Retrieve the information of Transaction by passed Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            # any additional logic
            serializer = TransactionDetailsSerializers(instance)

            return Response(serializer.data)
        

class NewsFeedViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
    DestroyModelMixin,
    CreateModelMixin
    ):
    """
    Send Push Notification 

    This endpoints allows you to send push notifications to kroon and kiosk users , using the notification ID to get and delete the notification that is stored

    """
 
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "id"
    serializer_class = AdminNewsFeedSerializer
    queryset = AdminNewsFeed.objects.all()
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['created_date', 'modified_date']
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

    def get_object(self, queryset=None):
        return AdminNewsFeed.objects.get(id=self.kwargs["id"])
    
    # Post Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Post Push Notifications",
        operation_description="Create and push Push Notifications.",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # sendout push notification
        device_push_notification(serializer = serializer)
        self.perform_create( serializer )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(publisher = self.request.user) # save the publisher
    
    
    # All Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="All Push Notifications",
        operation_description="Endpoints retrieves the list of Push Notifications.",
    )
    def list(self, request, *args, **kwargs):
        return super(NewsFeedViewSet, self).list(request, *args, **kwargs)
    
    # Get Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get Push Notifications",
        operation_description=" Retrieve the information of a push notification by passed Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            # any additional logic
            serializer = NotificationInfo(instance)
            return Response(serializer.data)
    
    # Delete Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Delete Push Notifications",
        operation_description="This deletes a push notification using the push notification ID",
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    

class ELearningViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
    DestroyModelMixin,
    CreateModelMixin
    ):
    """
    E-Learning  

    This endpoints allows you to publish tutorials videos to kroon and kiosk users , using each video ID to get and delete the any published clip that is stored to guild the users on how to use the application.

    """
 
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "id"
    serializer_class = ELearningSerializers
    queryset = Kiosk_E_Learning.objects.all()
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['created_date', 'modified_date']
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

    def get_object(self, queryset=None):
        return Kiosk_E_Learning.objects.get(id=self.kwargs["id"])
    
    # Post Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Upload Elearning Clip",
        operation_description="Create and uploads the elearning clip.",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        self.perform_create( serializer )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # def perform_create(self, serializer):
    #     serializer.save(publisher = self.request.user) # save the publisher
    
    
    # All Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="List of Elearning clips",
        operation_description="Endpoints retrieves the list of kroon and kiosk tutorial clips which is known as elearning.",
    )
    def list(self, request, *args, **kwargs):
        return super(ELearningViewSet, self).list(request, *args, **kwargs)
    
    # Get Uploaded Tutorial video
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get elearning clip",
        operation_description=" Retrieve the information of a video by passed Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            # any additional logic
            serializer = ElearningInfo(instance)
            return Response(serializer.data)
    
    # Delete Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Delete Elearning Video",
        operation_description="This deletes a elearning Video using the elearning VideoID",
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class SurveyViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin
    ):
    """
    Survey  

    This endpoints allows you to surveys to kroon and kiosk users , using each survey ID to get and delete the any published survey that is stored to get the ideas on how the users feel using the following applications under the kroon network .

    """
 
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "id"
    serializer_class = SurveyQuestionSerializer
    queryset = AppSurveyQuestion.objects.all()
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['created_date', 'modified_date']
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

    def get_object(self, queryset=None):
        return AppSurveyQuestion.objects.get(id=self.kwargs["id"])
    
    # Post Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Post Survey Question",
        operation_description="Create the survey questions for the users",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        self.perform_create( serializer )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # def perform_create(self, serializer):
    #     serializer.save(publisher = self.request.user) # save the publisher
    
    
    # All Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="List Survey Questions",
        operation_description="Endpoints retrieves the list of user that answred the following inapp ssurvey that is been published by the kroon network admin .",
    )
    def list(self, request, *args, **kwargs):
        return super(SurveyViewSet, self).list(request, *args, **kwargs)
    
    #Update survey questions
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Update a Survey Questions",
        operation_description="Update a survey question using the survey ID.",
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Patch update on a survey qestion
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Patch a Survey Questions",
        operation_description="Patch a  survey question using the survey ID.",
    )
    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # Get Uploaded Tutorial video
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get Survey Question",
        operation_description=" Retrieve the information of a survey by passing the survey Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            # any additional logic
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
    
    # Delete Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Delete Survey Question",
        operation_description="This deletes a survey question using the survey question ID",
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


    

class AnsweredSurveyViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
    DestroyModelMixin
    ):
    """
    Answered Survey  

    This endpoints allows the admin to get the list and delete the survey actions taken by the  kroon and kiosk users , using each survey ID to get and delete the any published survey that is stored to get the ideas on how the users feel using the following applications under the kroon network .

    """
 
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "id"
    serializer_class = SurveyUsers
    queryset = App_Survey.objects.all()
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['created_date', 'modified_date']
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

    def get_object(self, queryset=None):
        return SurveyQA.objects.get(survey_qa=self.kwargs["id"])
     
    
    # All Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="List Survey Users",
        operation_description="Endpoints retrieves the list of user that answred the following inapp ssurvey that is been published by the kroon network admin .",
    )
    def list(self, request, *args, **kwargs):
        return super(AnsweredSurveyViewSet, self).list(request, *args, **kwargs)

    
    # Get Uploaded Tutorial video
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get Survey QA",
        operation_description=" Retrieve the information of a survey by passing the survey Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            # any additional logic
            serializer = SurveyQuestioninfo(instance)
            return Response(serializer.data)
    
    # Delete Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Delete Survey QA",
        operation_description="This deletes a survey using the survey ID",
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.get_queryset().get( id = instance.survey_qa.id).delete()
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    




class InAppAdsViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin
    ):
    """
    Ad  

    This endpoints allows you to post in app ads to kroon and kiosk users , using each ad ID to get and delete the any published ad that is stored using the following applications under the kroon network .

    """
 
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "id"
    serializer_class = AdsSerializer
    queryset = Ads.objects.all()
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['created_date', 'modified_date']
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

    def get_object(self, queryset=None):
        return Ads.objects.get(id=self.kwargs["id"])
    
    # Post Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Post Ad",
        operation_description="Create the ads for the users",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        self.perform_create( serializer )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(status = True) # change the status to true
    
    
    # All Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="List Ads",
        operation_description="Endpoints retrieves the list of inapp ads  that is been published by the kroon network admin .",
    )
    def list(self, request, *args, **kwargs):
        return super(InAppAdsViewSet, self).list(request, *args, **kwargs)
    
    #Update ads
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Update a Ad",
        operation_description="Update a ad using the survey ID.",
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    # Patch update on a survey qestion
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Patch an Ads",
        operation_description="Patch an inapp ad using the survey ID.",
    )
    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    # Get Uploaded Tutorial video
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get Ad",
        operation_description=" Retrieve the an inapp  ad by passing the ad Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            # any additional logic
            serializer = AdsInfo(instance)
            return Response(serializer.data)
    
    # Delete Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Delete Ad",
        operation_description="This deletes an inapp  ad using the ad ID",
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class TotalTransactions(
    GenericViewSet
    ):
    """
    Get total of all transactions 

    This endpoint allows you to get all transactions been made by the users in kroon and kiosk

    A transaction details consists of the following TOPUP, Local Bank  WITHDRAWAL

    """
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter
    
    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields


    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total Transaction",
        operation_description=" this shows the amount of all transactions to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
                

        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # today = date.today()
        this_year = int(year)
        last_year = this_year - 1
 

        transaction_qs = Transactions.objects.select_related('user','benefactor','recipient').filter(Q(user__gender = gender.lower()) , user__country_of_residence = country_id  , status = "successful", created_date__year = this_year).values("status").annotate(total_amount=Sum('amount_in_localcurrency'))

        last_year_transaction_qs = Transactions.objects.select_related('user','benefactor','recipient').filter(Q(user__gender = gender.lower()) , user__country_of_residence = country_id  , status = "successful", created_date__year = last_year ).values("status").annotate(total_amount=Sum('amount_in_localcurrency'))

        total_amount = 0
        last_year_amount = 0

        # qs_percentage = transaction_qs.
        for transact in transaction_qs:
            if 'total_amount' in transact:
                total_amount = transact['total_amount']
            else:
                total_amount = 0

        for last_year_transact in last_year_transaction_qs:
            if 'total_amount' in last_year_transact:
                last_year_amount = last_year_transact['total_amount']
            else:
                last_year_amount = 0

        if last_year_amount != 0:
            percentage  = (total_amount - last_year_amount) / last_year_amount * 100
        else:
            percentage = 0

        percentage_format = "{}%".format(percentage)

        data = {
            'local_currency': country_id.currency.upper(),
            'total_amount': total_amount,
            'transaction_percentage': percentage_format,
            'last_year_amount':last_year_amount,
            'total_percentage':percentage_format
        }

        return Response(data , status=status.HTTP_200_OK)
    

class TotalWalletValue(GenericViewSet):
    """
    Get total wallet value 

    This endpoint allows you to get all the merchants total value , merchants using kroon 

    """
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter

    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total Wallet Value",
        operation_description="this shows the amount of all wallet value to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
                

        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # today = date.today()
        this_year = int(year)
        last_year = this_year - 1
 

        wallet_value = User.objects.select_related('country_province','country','on_boarding_user','government_organization_name','bank_details').filter(Q(gender = gender.lower()) , country_of_residence = country_id , created_date__year = this_year).values("is_active").annotate(total_amount=Sum('kroon_token'))

        last_year_wallet_value = User.objects.select_related('country_province','country','on_boarding_user','government_organization_name','bank_details').filter(Q(gender = gender.lower()) , country_of_residence = country_id , created_date__year = last_year ).values("is_active").annotate(total_amount=Sum('kroon_token'))

        total_amount = 0
        last_year_amount = 0

        # qs_percentage = wallet_value.
        for transact in wallet_value:
            if 'total_amount' in transact:
                total_amount = transact['total_amount']
            else:
                total_amount = 0

        for last_year_transact in last_year_wallet_value:
            if 'total_amount' in last_year_transact:
                last_year_amount = last_year_transact['total_amount']
            else:
                last_year_amount = 0

        if last_year_amount != 0:
            percentage  = (total_amount - last_year_amount) / last_year_amount * 100
        else:
            percentage = 0
        
        percentage_format = "{}%".format(percentage)

        
        data = {
            'local_currency': country_id.currency.upper(),
            'total_amount': total_amount,
            'transaction_percentage': percentage_format,
            'last_year_amount':last_year_amount,
            'total_percentage':percentage_format
        }

        return Response(data , status=status.HTTP_200_OK)

    


class TotalPayouts(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter

    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields


    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total Payouts",
        operation_description=" this shows the amount of all payouts to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
                

        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # today = date.today()
        this_year = int(year)
        last_year = this_year - 1
 

        total_payout = Transactions.objects.select_related('user','benefactor','recipient').filter(Q(user__gender = gender.lower()) , user__country_of_residence = country_id  , status = "successful", created_date__year = this_year  , action = "LOCAL BANK WITHDRAWAL" ).values("status").annotate(total_amount=Sum('debited_kroon_amount'))

        last_year_total_payout = Transactions.objects.select_related('user','benefactor','recipient').filter(Q(user__gender = gender.lower()) , user__country_of_residence = country_id  , status = "successful", created_date__year = last_year , action = "LOCAL BANK WITHDRAWAL" ).values("status").annotate(total_amount=Sum('debited_kroon_amount'))

        total_amount = 0
        last_year_amount = 0

        # qs_percentage = wallet_value.
        for transact in total_payout:
            if 'total_amount' in transact:
                total_amount = transact['total_amount']
            else:
                total_amount = 0

        for last_year_transact in last_year_total_payout:
            if 'total_amount' in last_year_transact:
                last_year_amount = last_year_transact['total_amount']
            else:
                last_year_amount = 0

        if last_year_amount != 0:
            percentage  = (total_amount - last_year_amount) / last_year_amount * 100
        else:
            percentage = 0
        
        percentage_format = "{}%".format(percentage)

        
        data = {
            'local_currency': country_id.currency.upper(),
            'total_amount': total_amount,
            'transaction_percentage': percentage_format,
            'last_year_amount':last_year_amount,
            'total_percentage':percentage_format
        }

        return Response(data , status=status.HTTP_200_OK)
    

class TotalEwallets(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter

    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total E-Wallets",
        operation_description=" this shows the amount of all E wallets to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
                

        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # today = date.today()
        this_year = int(year)
        last_year = this_year - 1
 

        total_ewallet = User.objects.select_related('country_province','country','on_boarding_user','government_organization_name','bank_details').filter(Q(gender = gender.lower()) , country_of_residence = country_id , created_date__year = this_year).values("is_active").annotate(total_amount=Count('is_active'))

        last_year_total_ewallet = User.objects.select_related('country_province','country','on_boarding_user','government_organization_name','bank_details').filter(Q(gender = gender.lower()) , country_of_residence = country_id , created_date__year = last_year ).values("is_active").annotate(total_amount=Count('is_active'))


        total_amount = 0
        last_year_amount = 0

        # qs_percentage = total_ewallet.
        for transact in total_ewallet:
            if 'total_amount' in transact:
                total_amount = transact['total_amount']
            else:
                total_amount = 0

        for last_year_transact in last_year_total_ewallet:
            if 'total_amount' in last_year_transact:
                last_year_amount = last_year_transact['total_amount']
            else:
                last_year_amount = 0

        # if last_year_amount != 0:
        #     percentage  = (total_amount - last_year_amount) / last_year_amount * 100
        # else:
        #     percentage = 0
        
        # percentage_format = "{}%".format(percentage, '.2f')

        
        data = {
            'total_wallet': total_amount, #total ewallet
            'last_year_wallet':last_year_amount, #total ewallet last year
        }

        return Response(data , status=status.HTTP_200_OK)
    


class TotalMerchants(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter

    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total Merchants",
        operation_description=" this shows the amount of all registered merchants to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
                
        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # today = date.today()
        this_year = int(year)
        last_year = this_year - 1
 
        total_merchant = User.objects.select_related('country_province','country','on_boarding_user','government_organization_name','bank_details').filter(Q(gender = gender) , country_of_residence = country_id , created_date__year = this_year , account_type = "merchant").values("is_active").annotate(total_amount=Count('is_active'))

        last_year_total_merchant = User.objects.select_related('country_province','country','on_boarding_user','government_organization_name','bank_details').filter(Q(gender = gender) , country_of_residence = country_id , created_date__year = last_year , account_type = "merchant" ).values("is_active").annotate(total_amount=Count('is_active'))


        total_amount = 0
        last_year_amount = 0

        # qs_percentage = total_ewallet.
        for transact in total_merchant:
            if 'total_amount' in transact:
                total_amount = transact['total_amount']
            else:
                total_amount = 0

        for last_year_transact in last_year_total_merchant:
            if 'total_amount' in last_year_transact:
                last_year_amount = last_year_transact['total_amount']
            else:
                last_year_amount = 0

        data = {
            'total_merchants': total_amount,
            'last_year_merchants':last_year_amount,
        }

        return Response(data , status=status.HTTP_200_OK)
    


class CrossBorderTransfer(GenericViewSet):
    #TODO: cross border transfer need to be fixed by allowing cross border transfer
    permission_classes = [
        AllowAny,
        # KOKPermission,
        # IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Cross Border Transfer",
        operation_description=" *SANDBOX* // this shows the amount of all cross border transfer to compare last year record ",
    )
    def list(self, request, *args, **kwargs):

        data = {
            'local_currency': 'NGN',
            'total_cross_border_transfers': 453928,
            'last_year_cross_border_transfers':36392124,
        }

        return Response(data , status=status.HTTP_200_OK)
    

class DailyAverage(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter

    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields
    

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Daily Average",
        operation_description="this shows the amount of all daily average to compare yesterday record",
    )
    def list(self, request, *args, **kwargs):
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
   

        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        today = date.today()
        yesterday = today - timedelta(days=1)

        today_qs = Transactions.objects.select_related('user','benefactor','recipient').filter(Q(user__gender = gender.lower()) , user__country_of_residence = country_id  , status = "successful", created_date__date = today  )

        today_volume = today_qs.count()
        total_payout = today_qs.values("status").annotate(total_amount=Sum('amount_in_localcurrency'))

        yesterday_qs = Transactions.objects.select_related('user','benefactor','recipient').filter(Q(user__gender = gender.lower()) , user__country_of_residence = country_id  , status = "successful", created_date__date = yesterday )

        yesterday_volume = yesterday_qs.count()
        yesterday_transacts = yesterday_qs.values("status").annotate(total_amount=Sum('amount_in_localcurrency'))


        total_amount = 0
        yesterday_amount = 0

        # qs_percentage = wallet_value.
        for transact in total_payout:
            if 'total_amount' in transact:
                total_amount = transact['total_amount']
            else:
                total_amount = 0

        for yesterday_transact in yesterday_transacts:
            if 'total_amount' in yesterday_transact:
                yesterday_amount = yesterday_transact['total_amount']
            else:
                yesterday_amount = 0

        if yesterday_amount != 0:
            percentage  = (total_amount - yesterday_amount) / yesterday_amount * 100
        else:
            percentage = 0
        
        percentage_format = "{}%".format(percentage)


        percentage_volume = 0
        if yesterday_volume != 0:
            percentage_volume  = (today_volume - yesterday_volume) / yesterday_volume * 100
        else:
            percentage_volume = 0
        
        percentage_format_value = "{}%".format(percentage_volume)
        percentage_format = "{}%".format(percentage)


        response = {
            'local_currency': country_id.currency.upper(),
            # today transaction and value
            'transaction_volume': today_volume,
            'yesterday_transaction_volume':yesterday_volume,
            'transaction_volume_per': percentage_format_value,
            # yesterday transaction and value
            'transaction_value': total_amount,
            'yesterday_transaction_value':yesterday_amount,
            'transaction_value_per': percentage_format
        }

        return Response(data=response , status=status.HTTP_200_OK)
    

class TotalActiveMerchants(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter

    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields


    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Active Merchants",
        operation_description=" this shows the total count of all merchants both the new and loss merchants on the platform ",
    )
    def list(self, request, *args, **kwargs):
        
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
                
        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # today = date.today()
        this_year = int(year)
        #TODO:#fixing the gender selection for all 
        merchant_qs = User.objects.select_related('country_province','country','on_boarding_user','government_organization_name','bank_details').filter(Q(gender = gender) , country_of_residence = country_id , created_date__year = this_year )

        active_merchant = merchant_qs.filter( is_active = True ).count()
        inactive_merchant = merchant_qs.filter( is_active = False ).count()


        data = {
            'new_merchants':active_merchant,
            'loss_merchants':inactive_merchant
        }

        return Response(data , status=status.HTTP_200_OK)
    

class GlobalOverview(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Country_Province.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter
    pagination_class = StandardResultsSetPagination
    lookup_field = "id"

    def get_object(self, queryset=None):
        return Country_Province.objects.get(id=self.kwargs["id"])

    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields
    

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Global Overview",
        operation_description="This shows the list of global Overview",
    )
    def list(self, request, *args, **kwargs):
        
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
                
        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        
        list_of_province = Country_Province.objects.select_related('country').filter(country = country_id)

        all_active_user = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details').filter( country_of_residence = country_id , is_active = True )


        province_list = []
        for i in list_of_province:
            # user query set
            user_qs = User.objects.select_related('country_of_residence', 'country_province').filter(country_province = i.id, is_active = True)

            province_users = User.objects.select_related('country_of_residence', 'country_province').filter(country_province = i.id, is_active = True).count()
    
            province_merchant_sales = Order.objects.select_related("user", "payment").filter( user__country_province = i.id,user__is_active = True, is_ordered = True ).count()

            total_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user__country_province = i.id, ordered = True )

            total_payout = Transactions.objects.select_related('user','benefactor','recipient').filter( user__country_province = i.id  , status = "successful" , action = "LOCAL BANK WITHDRAWAL" ).values("status").annotate(total_amount=Sum('debited_kroon_amount'))

            total_sale = 0 
            cost_of_sales_province = 0
            wallet_value = 0
            total_payout_amount = 0

            # merchant sales via province 
            for c in total_sales:
                total_sale += c.product_total_price

            # merchant cost of sales via province
            for c in total_sales:
                cost_of_sales_province += c.product.cost_price

            for v in user_qs:
                wallet_value += v.kroon_token

            # qs_percentage = wallet_value.
            for transact in total_payout:
                if 'total_amount' in transact:
                    total_payout_amount = transact['total_amount']
                else:
                    total_payout_amount = 0


            note = {
                'id': i.id,
                'local_currency': country_id.currency.upper(),
                'region':i.province , 
                'total_wallets':province_users , 
                'wallets_value': wallet_value, 
                'payout_value':total_payout_amount , 
                'total_merchants':province_users , 
                'active_merchants':province_users , 
                'merchant_sales_count':province_merchant_sales , 
                'merchant_revenue':total_sale , 
                'inventory_on_hand':cost_of_sales_province,
                'avg_transaction_value':cost_of_sales_province #TODO:fix this
                }
            province_list.append(note)

        # page = self.get_paginated_response(province_list)
        # if page is not None:
        # return self.paginator(province_list) #TODO:add pagination support

        # remote_username = request.META.get('USER')
        # remote_ipaddr = request.META.get('REMOTE_ADDR')
        # remote_os = request.META.get('HTTP_USER_AGENT')

        # print(remote_username)
        # print(remote_ipaddr)
        # print(remote_os)
        
        return Response(province_list , status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get Stores",
        operation_description="This shows the list of stores associated with the province or state id ",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
             instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            # any additional logic
            merchant_business_qs = BusinessProfile.objects.select_related('user').filter( user__country_province = instance.id )

            page = self.paginate_queryset(merchant_business_qs)
            if page is not None:
                serializer = BusinessProfileSerilizer(page , many = True )
                return self.get_paginated_response(serializer.data)
        
            return Response(serializer.data , status=status.HTTP_200_OK)



class GlobalSales(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter

    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields
    

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Global Sales",
        operation_description="This shows the global sales of a particular country",
    )
    def list(self, request, *args, **kwargs):
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
                
        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

        total_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user__country_of_residence = country_id , ordered = True , created_date__year = year )

        total_sale = 0
        cost_of_sales_global = 0
        # merchant sales via province 
        for c in total_sales:
            total_sale += c.product_total_price

        # merchant cost of sales via province
        for c in total_sales:
            cost_of_sales_global += c.product.cost_price 

        data = {
            'currency':country_id.currency,
            'total_sale':total_sale,
            'cost_of_sales_global':cost_of_sales_global
        }
        
        return Response(data , status=status.HTTP_200_OK)



class TransactionChannels (GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter

    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields
    

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Transaction Channels",
        operation_description="This shows the global payment channels used in a particular country",
    )
    def list(self, request, *args, **kwargs):
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
                
        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        transactions_channels_qs = Order.objects.select_related('user', 'payment').filter( user__country_of_residence = country_id , is_ordered = True , created_date__year = year ).values("payment__payment_method").annotate(total_amount=Sum('order_total'))

        return Response({'currency':country_id.currency ,'data':transactions_channels_qs }, status=status.HTTP_200_OK)



class CategorySales(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminRecordFilter

    def get_filterinputs(self):
        filter_fields = []
        filterset_data = self.filterset_class
        # Instantiate the filterset
        filterset = filterset_data(data=self.request.query_params, queryset=self.queryset)
        # List out the filter inputs
        filter_inputs = filterset.data
        # You can now iterate through filter_inputs to list them out
        for key , value in filter_inputs.items():
            filter_fields.append({
               f"{key}":f"{value}"
                })
        return filter_fields
    

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Transaction Channels",
        operation_description="This shows the global payment channels used in a particular country",
    )
    def list(self, request, *args, **kwargs):
        data = self.get_filterinputs()

        country = None
        gender = None
        year = None
        # Loop through the list of dictionaries
        for item in data:
            if 'country' in item:
                country = item['country']
                pass  # Stop searching if 'country' is found

            if 'gender' in item:
                gender = item['gender'].lower()
                pass  # Stop searching if 'gender' is found
            
            if 'year' in item:
                year = item['year']
                pass
                
        # Now 'country' contains the value if found, or it's None if not found
        try:
            country_id = Country.objects.get(iso2=country.upper())
        except Country.DoesNotExist:
            return Response({'message': 'Country ISO2 does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        category_sales_qs = Order.objects.select_related('user', 'payment').filter( user__country_of_residence = country_id , is_ordered = True , created_date__year = year ).values("products__category__category").annotate(total_amount=Sum('order_total'))

        return Response({'currency':country_id.currency ,'data':category_sales_qs } , status=status.HTTP_200_OK)


class BusinessRecords(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    lookup_field = "id"

    def get_object(self, queryset=None):
        return BusinessProfile.objects.get(id=self.kwargs["id"])
    
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Retrive Stores",
        operation_description="This retrives the store sales and records by passing the store ID ",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
             instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            # any additional logic
            merchant_business_qs = BusinessProfile.objects.select_related('user').get( id = instance.id )    
            
            business_owner = merchant_business_qs.user
            # store transactional channels 
            order_qs = Order.objects.select_related('user', 'payment').filter( is_ordered = True , user = business_owner )

            # latest sales invoice 
            latest_sales_invoice = order_qs.values("order_number", "order_total", "created_date__date", "payment__payment_method")[:5]

            transactions_channels_qs = order_qs.values("payment__payment_method").annotate(total_amount=Sum('order_total'))

            # total sales and cost prices 
            total_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( ordered = True , user = business_owner )

            daily_sales_qs = total_sales.values("created_date__date").annotate(total_amount = Sum('product_total_price'))[:10]

            total_sale = 0
            cost_of_sales = 0
            # merchant sales via province 
            for c in total_sales:
                total_sale += c.product_total_price

            # merchant cost of sales via province
            for c in total_sales:
                cost_of_sales += c.product.cost_price 

            # category sales and total amount records
            category_sales_qs = Order.objects.select_related('user', 'payment').filter(user = business_owner , is_ordered = True ).values("products__category__category").annotate(total_amount=Sum('order_total'))

            # business workers
            workers_qs = BusinessProfile.objects.select_related('user').filter( id = instance.id ).values("workers").count()
           

            serializer = BusinessProfileSerilizer( merchant_business_qs )

            data = {
                "currency_id":business_owner.default_currency_id,
                "business_info":serializer.data,
                "daily_sales": daily_sales_qs,
                "sales_record":{
                    "total_sale":total_sale,
                    "cost_of_sales":cost_of_sales
                },
                "category_sales":category_sales_qs,
                "transactional_channels":transactions_channels_qs,
                "employee_count": workers_qs,
                "latest_sales_invoice":latest_sales_invoice
            }
            
            return Response(data , status=status.HTTP_200_OK)
    