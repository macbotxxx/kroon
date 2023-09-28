from rest_framework import  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from datetime import timedelta, datetime
from datetime import date
from django.db.models import Count , Sum



from helpers.common.security import KOKPermission, KOKMerchantPermission
from kroon.users.models import User
from kroon.users.models import BusinessProfile
from .serializers import CreateWorkersAccount, WorkerProfileSerializer
from kiosk_cart.models import  Order


class CreateWorkersAccountView (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = CreateWorkersAccount

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)

            # adding the new worker the companys account as a worker 
            merchant_business = BusinessProfile.objects.get ( user = request.user , active = True)
            merchant_business.workers.add(user)
            
            return Response({'status':'success', 'message':'account is been created successfully'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class CheckWorkerEmailView (ListAPIView):
    permission_classes =  [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = WorkerProfileSerializer

    def get(self, request, *args, **kwargs):
        email = kwargs.get('email')
        # checking if user email address is registered
        try:
            user_record = User.objects.get( email=email )
            serializer = self.serializer_class( user_record )
            return Response({'status':'success','message':'worker account is fetched succesfully.', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
            
        except User.DoesNotExist:
            return Response({'status':'error', 'message':'user is not a registered user'}, status= status.HTTP_404_NOT_FOUND)


class All_Workers ( ListAPIView ):
    permission_classes = [ IsAuthenticated , KOKPermission , KOKMerchantPermission ]
    serializer_class = WorkerProfileSerializer
    queryset = BusinessProfile.objects.select_related('user').all()

    def get (self, request, *args, **kwargs):
        my_worker = self.get_queryset().filter( user = self.request.user , active = True )
        for w in my_worker:
            workers = w.workers
        
        serializer = self.serializer_class( workers , many = True )
         # return function response
        return Response({ 'status':'successful', 'message':'workers list is fetched successfully', 'data':serializer.data }, status=status.HTTP_200_OK )
    

class Worker_Details ( APIView ):
    
    permission_classes = [ IsAuthenticated , KOKPermission , KOKMerchantPermission ]
    serializer_class = None
    qs = BusinessProfile.objects.select_related('user').all()
    
    def get (self, request, *args, **kwargs):
        email = kwargs.get('email')
        weekly_days = 7
        workers_weekly_days = []
        # worker_name = None
        worker_report = []
        # filtering and validating worker details 
        my_worker = self.qs.filter( user = self.request.user , active = True , workers__email = email )
        if not my_worker:
            return Response({'status':'error', 'message':'worker email account is not associated to the merchant business account', 'data':[]} , status=status.HTTP_404_NOT_FOUND )
        
        # getting the worker name 
        worker_name = User.objects.get( email = email )

        for i in range(weekly_days):
            Previous_Date = date.today()  - timedelta(days=i)
            workers_weekly_days.append(Previous_Date.strftime("%d %b"))

            sale_reports = Order.objects.select_related("user", "payment").filter( worker = worker_name.name , is_ordered = True , created_date__date  = Previous_Date ).values('worker').annotate(total_sales_amount = Sum('order_total') , total_sales_count = Count('is_ordered')).order_by('-is_ordered')
            # append workers report
            worker_report.append( sale_reports )
        
        data = { 'workers_weekly_days':workers_weekly_days,'worker_report':worker_report }

        return Response({'status': 'successful','message':'workers details and sales reports', 'data': data}, status=status.HTTP_202_ACCEPTED)
    


    def delete( self, request, *args, **kwargs ):
        # worker email address
        email = kwargs.get('email')
        # filtering and validating worker details 
        try:
            my_worker = self.qs.get( user = self.request.user , active = True , workers__email = email )
        except  BusinessProfile.DoesNotExist:
            return Response({'status':'error', 'message':'worker email account is not associated to the merchant business account', 'data':[]} , status=status.HTTP_404_NOT_FOUND )
        
        user_profile_set = User.objects.get ( email  = email )
        my_worker.workers.remove(user_profile_set)

        return Response({'status':'successful', 'message':f"{user_profile_set} has been removed from your business profile successfully ", 'data':[] } , status=status.HTTP_200_OK )
    

class Add_Worker_VIew ( APIView ):
    permission_classes = [ IsAuthenticated , KOKPermission , KOKMerchantPermission ]
    serializer_class = None
    qs = BusinessProfile.objects.select_related('user').all()

    def post(self,request ,*args, **kwargs):
        # worker email address
        email = kwargs.get('email')
        # filtering and validating worker details
        try:    
            user_profile_set = User.objects.get ( email = email )
        except User.DoesNotExist:
            return Response({'status':'error', 'message':'user is not a registered user'}, status= status.HTTP_404_NOT_FOUND)

        # adding the new worker the companys account as a worker
        try:
            self.qs.get( workers = user_profile_set )
            return Response({'status':'error', 'message': f"Kindly contact your worker to resign from his or her former employee, so to be able to continue.", 'data':[]}, status=status.HTTP_400_BAD_REQUEST)

        except BusinessProfile.DoesNotExist:
            pass

        merchant_business = self.qs.get( user = request.user, active = True )
        merchant_business.workers.add(user_profile_set)
        
        return Response({'status':'successful', 'message': f"{user_profile_set} has been added to your business profile successfully ", 'data':[]}, status=status.HTTP_200_OK )

       
