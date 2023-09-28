from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, get_object_or_404
import datetime
from helpers.common.security import KOKPermission

from kroon.users.models import User


from .serializers import KYCSerializer, MarchantKycApplicationSerializer
from kroon_kyc.models import KycApplication, MarchantKycApplication


class KYCView (ListAPIView, CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = KYCSerializer

    def get(self, request, *args, **kwargs):
        user_kyc = get_object_or_404(KycApplication, user = request.user)
        serializer = self.serializer_class(user_kyc)
        return Response({'status':'success','message':'customers KYC is fetched successfully','data':serializer.data}, status=status.HTTP_202_ACCEPTED)

    def post(self, request, *args, **kwargs):
        serializer = KYCSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            user_kyc = User.objects.get(id = request.user.id)
            user_kyc.kyc_complete = True
            user_kyc.kyc_submitted = True
            user_kyc.kyc_complete_date = datetime.datetime.now()
            user_kyc.save()
            return Response({'status':'success','message':'customers KYC is been submitted successfully','data':serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'status':'error','message':'failed to input the following request','data':serializer.errors},  status=status.HTTP_400_BAD_REQUEST)



class MarchantKYCVIEW (ListAPIView, CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = MarchantKycApplicationSerializer

    def get(self, request, *args, **kwargs):
        user_kyc = get_object_or_404(MarchantKycApplication, user = request.user)
        serializer = self.serializer_class(user_kyc)
        return Response({'status':'success','message':'customers KYC is fetched successfully','data':serializer.data}, status=status.HTTP_202_ACCEPTED)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            
            if MarchantKycApplication.objects.filter(user = request.user).exists():
                return Response({'status':'error','message':'user has already submitted a kyc form '}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            user_kyc = User.objects.get(id = request.user.id)
            user_kyc.kyc_complete = True
            user_kyc.kyc_submitted = True
            user_kyc.kyc_complete_date = datetime.datetime.now()
            user_kyc.save()
            return Response({'status':'success','message':'customers KYC is been submitted successfully','data':serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



