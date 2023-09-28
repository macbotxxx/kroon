import datetime
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView , RetrieveDestroyAPIView , CreateAPIView
from helpers.common.security import KOKPermission
from drf_yasg.utils import swagger_auto_schema
from kroon.users.models import User , BusinessProfile
from .serializers import BusinessAgreementsSerializer , AgreementsInfoSerializer , SharesAgreementSerializer , GoodsAndServicesAgreementSerailizer , Loan_AgreementSerailizer 

from kiosk_agreements.models import Business_Agreements , Agreements_Info , Shares_Agreements , Goods_And_Services_Agreement , Loan_Agreement , Shares_Signatures



class BusinessAgreementsView(ListAPIView):
    permission_classes = [IsAuthenticated , KOKPermission,]
    queryset = Business_Agreements.objects.all()
    serializer_class = BusinessAgreementsSerializer
    lookup_field = 'id'
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    ordering_fields = ['created_date', 'modified_date']



class AgreementsInfoListView( RetrieveDestroyAPIView ):
    permission_classes = [IsAuthenticated , KOKPermission,]
    queryset = Agreements_Info.objects.all()
    serializer_class = AgreementsInfoSerializer
    lookup_field = 'id'
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    ordering_fields = ['created_date', 'modified_date']


class AgreementsInfoView( CreateAPIView , ListAPIView ):
    permission_classes = [IsAuthenticated , KOKPermission,]
    queryset = Agreements_Info.objects.all()
    serializer_class = AgreementsInfoSerializer
    ordering_fields = ['created_date', 'modified_date']


    def perform_create(self, serializer):
        # getting the business information
        try:
            business_info = BusinessProfile.objects.get( user = self.request.user , active = True )
        except BusinessProfile.DoesNotExist:
            return Response({'status':'error','message':'business account does not exist'}, status = status.HTTP_404_NOT_FOUND )
        serializer.save( user = self.request.user , business_logo = business_info.business_logo )

    
    @swagger_auto_schema(
            responses={404: 'business account does not exist'},
            operation_summary="List of Agreements Info",
            operation_description="List of all Agreements that is been registered and submitted",
            )
    def get (self, request, *args, **kwargs):
        agreement = self.get_queryset().filter(user = self.request.user)
        serializer = self.get_serializer(agreement , many = True)
        return Response( serializer.data )
    

    # @swagger_auto_schema(
    #         operation_summary="Create Agreements Info",
    #         operation_description="""
    #         POST /articles/{id}/image/
    #         This allows the ability to create business agreement information,
    #         Agreement information typically refers to the details and specifics contained within a particular agreement. It encompasses the relevant information, terms, conditions, and provisions outlined in the agreement that define the rights, responsibilities, and obligations of the parties involved.
    #         """, 
    #         )
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    


    

class AllAgreementView(  ListAPIView ):
    permission_classes = [IsAuthenticated , KOKPermission,]
    queryset = Shares_Agreements.objects.all()
    serializer_class = SharesAgreementSerializer
    ordering_fields = ['created_date', 'modified_date']

    def list (self, request, *args, **kwargs):
        agreement = self.get_queryset().filter(user = self.request.user)
        share_agreements = self.get_serializer( agreement , many = True)
        
        ea = Agreements_Info.objects.filter(user = self.request.user)
        employee_agreement = AgreementsInfoSerializer( ea, many = True )

        gnds = Goods_And_Services_Agreement.objects.filter(user = self.request.user)
        lgs = Loan_Agreement.objects.filter(user = self.request.user)

        good_n_service = GoodsAndServicesAgreementSerailizer(gnds , many = True)
        loans_agreements = Loan_AgreementSerailizer( lgs , many = True )

        data = {
            'share_agreements':share_agreements.data,
            'good_n_service': good_n_service.data,
            'loans_agreements': loans_agreements.data,
            'employee_agreement':employee_agreement.data,
        }

        return Response( data )
    



class SharesAgreementView( CreateAPIView , ListAPIView ):
    permission_classes = [IsAuthenticated , KOKPermission,]
    queryset = Shares_Agreements.objects.all()
    serializer_class = SharesAgreementSerializer
    ordering_fields = ['created_date', 'modified_date']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data )
        if serializer.is_valid():

            # getting the business information
            try:
                business_info = BusinessProfile.objects.get( user = self.request.user , active = True )
            except BusinessProfile.DoesNotExist:
                return Response({'status':'error','message':'business account does not exist'}, status = status.HTTP_404_NOT_FOUND )
            
            company_name = serializer.validated_data.get('company_name')
            company_country = serializer.validated_data.get('company_country')
            company_share = serializer.validated_data.get('company_share')
            owner_name = serializer.validated_data.get('owner_name')
            non_compete_period = serializer.validated_data.get('non_compete_period')
            signature = serializer.validated_data.get('signature')
            formatted_date = serializer.validated_data.get('formatted_date')
            share_signatures = serializer.validated_data.get("share_holders")

            shares_arg = Shares_Agreements()
            shares_arg.company_name = company_name
            shares_arg.company_country = company_country
            shares_arg.company_share = company_share
            shares_arg.owner_name = owner_name
            shares_arg.non_compete_period = non_compete_period
            shares_arg.signature = signature
            shares_arg.business_logo = business_info.business_logo
            shares_arg.formatted_date = formatted_date
            shares_arg.user = self.request.user
            shares_arg.save()

            for i in share_signatures:
                signature = Shares_Signatures()
                signature.name = i["name"]
                signature.address = i["address"]
                signature.share = i["share"]
                signature.share_price = i["share_price"]
                if i["shares_signature"] is not None:
                    signature.shares_signature = i["shares_signature"]
                signature.agreements = shares_arg
                signature.save()
                shares_arg.share_holders.add(signature)
            return Response(serializer.data)
        
    def list (self, request, *args, **kwargs):
        agreement = self.get_queryset().filter(user = self.request.user)
        serializer = self.get_serializer( agreement , many = True)
        return Response( serializer.data )


class SharesAgreementListView( RetrieveDestroyAPIView ):
    permission_classes = [IsAuthenticated , KOKPermission,]
    queryset = Shares_Agreements.objects.all()
    serializer_class = SharesAgreementSerializer
    lookup_field = 'id'
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    ordering_fields = ['created_date', 'modified_date'] 


class GoodsAndServicesAgreementView( CreateAPIView , ListAPIView):
    permission_classes = [IsAuthenticated , KOKPermission,]
    queryset = Goods_And_Services_Agreement.objects.all()
    serializer_class = GoodsAndServicesAgreementSerailizer
    ordering_fields = ['created_date', 'modified_date']

    def perform_create(self, serializer):
        # getting the business information
        try:
            business_info = BusinessProfile.objects.get( user = self.request.user , active = True )
        except BusinessProfile.DoesNotExist:
            return Response({'status':'error','message':'business account does not exist'}, status = status.HTTP_404_NOT_FOUND )
        
        serializer.save( user = self.request.user , business_logo = business_info.business_logo )

    def list (self, request, *args, **kwargs):
        agreement = self.get_queryset().filter(user = self.request.user)
        serializer = self.get_serializer( agreement , many = True)
        return Response( serializer.data )


class GoodsAndServicesAgreementListView( RetrieveDestroyAPIView ):
    permission_classes = [IsAuthenticated , KOKPermission,]
    queryset = Goods_And_Services_Agreement.objects.all()
    serializer_class = GoodsAndServicesAgreementSerailizer
    lookup_field = 'id'
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    ordering_fields = ['created_date', 'modified_date'] 


class LoanAgreementView( CreateAPIView , ListAPIView ):
    permission_classes = [IsAuthenticated , KOKPermission,]
    queryset = Loan_Agreement.objects.all()
    serializer_class = Loan_AgreementSerailizer
    ordering_fields = ['created_date', 'modified_date']

    def perform_create(self, serializer):
        try:
            business_info = BusinessProfile.objects.get( user = self.request.user , active = True )
        except BusinessProfile.DoesNotExist:
            return Response({'status':'error','message':'business account does not exist'}, status = status.HTTP_404_NOT_FOUND )
        
        serializer.save( user = self.request.user , business_logo = business_info.business_logo )

    def list (self, request, *args, **kwargs):
        agreement = self.get_queryset().filter(user = self.request.user)
        serializer = self.get_serializer( agreement , many = True)
        return Response( serializer.data )
    

class LoanAgreementViewListView( RetrieveDestroyAPIView ):
    permission_classes = [IsAuthenticated , KOKPermission,]
    queryset = Loan_Agreement.objects.all()
    serializer_class = Loan_AgreementSerailizer
    lookup_field = 'id'
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    ordering_fields = ['created_date', 'modified_date']
