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
from datetime import date
from kroon.users.pagination import StandardResultsSetPagination
from helpers.common.security import KOKPermission
from kroon.users.models import User
from admin_reports.models import AdminNewsFeed
from admin_reports.task import device_push_notification
from admin_reports.permissions import IsBlekieAndEtransac
from e_learning.models import Kiosk_E_Learning , App_Survey, SurveyQA , AppSurveyQuestion
from ads.models import Ads
from locations.models import Country



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

        if last_year_amount != 0:
            percentage  = (total_amount - last_year_amount) / last_year_amount * 100
        else:
            percentage = 0
        
        percentage_format = "{}%".format(percentage, '.2f')

        
        data = {
            'local_currency': country_id.currency.upper(),
            'total_ewallet': total_amount, #total ewallet
            'transaction_percentage': percentage_format,
            'last_year_ewallet':last_year_amount, #total ewallet last year
            'total_percentage':percentage_format
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

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total Merchants",
        operation_description=" this shows the amount of all registered merchants to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = {
            'total_merchants': 8901,
            'last_year_merchants':2793,
        }

        return Response(data , status=status.HTTP_200_OK)
    


class CrossBorderTransfer(GenericViewSet):
   
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

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Daily Average",
        operation_description=" *SANDBOX* // this shows the amount of all daily average to compare yesterday record",
    )
    def list(self, request, *args, **kwargs):
        response = {
            'local_currency': 'NGN',
            'transaction_volume': 23678,
            'transaction_volume_per': '+17,82',
            'yesterday_transaction_volume':12984,
            'transaction_value': 40350,
            'transaction_value_per': '+13,20',
            'yesterday_transaction_value':20341,
        }

        return Response(data=response , status=status.HTTP_200_OK)
    

class TotalActiveMerchants(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Daily Average",
        operation_description=" *SANDBOX* // this shows the total count of all merchants both the new and loss merchants on the platform ",
    )
    def list(self, request, *args, **kwargs):
        data = {
            'new_merchants':10456,
            'loss_merchants':2450
        }

        return Response(data , status=status.HTTP_200_OK)
    


class TopPerformingRegions(GenericViewSet):
  
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Top Performing Regions",
        operation_description=" *SANDBOX* // this shows the list of top performing regions",
    )
    def list(self, request, *args, **kwargs):
        data = [
            {
                'region': 'Lagos',
                'transaction_value': 29321490,
            },
            {
                'region': 'Abuja',
                'transaction_value': 19300250,
            },
            {
                'region': 'Kano',
                'transaction_value': 17322822,
            }
        ]

        return Response(data , status=status.HTTP_200_OK)
    


class GlobalOverview(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Top Performing Regions",
        operation_description=" *SANDBOX* // this shows the list of top performing regions",
    )
    def list(self, request, *args, **kwargs):
        data = [
            {
                'region': 'Lagos',
                'local_currency': 'NGN',
                'total_wallets': 2046,
                'total_ewallet': 893876,
                'payout_value': 45723,
                'total_merchants': 2046,
                'active_merchants': 2046,
                'merchants_revenue': 29321490,
                'inventory_on_hand': 9321490,
                'avg_transactions': 60,
            },
            {
                'region': 'FCT Abuja',
                'local_currency': 'NGN',
                'total_wallets': 2046,
                'wallet_value': 893876,
                'payout_value': 45723,
                'total_merchants': 2046,
                'active_merchants': 2046,
                'merchants_revenue': 29321490,
                'inventory_on_hand': 9321490,
                'avg_transactions': 60,
            },
            {
                'region': 'Oyo',
                'local_currency': 'NGN',
                'total_wallets': 2046,
                'wallet_value': 893876,
                'payout_value': 45723,
                'total_merchants': 2046,
                'active_merchants': 2046,
                'merchants_revenue': 29321490,
                'inventory_on_hand': 9321490,
                'avg_transactions': 60,
            },
            {
                'region': 'Abia',
                'local_currency': 'NGN',
                'total_wallets': 2046,
                'wallet_value': 893876,
                'payout_value': 45723,
                'total_merchants': 2046,
                'active_merchants': 2046,
                'merchants_revenue': 29321490,
                'inventory_on_hand': 9321490,
                'avg_transactions': 60,
            },
           
        ]

        return Response(data , status=status.HTTP_200_OK)
    

# this is recorded to be a sandbox to the original data and records
# sandbox end here ----------------------------------------------------------------

    
    

        

    