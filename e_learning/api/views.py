from rest_framework import  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView, UpdateAPIView
from helpers.common.security import KOKPermission, KOKMerchantPermission, KOKMerchantOnly

from .serializers import E_LearningSerializer, App_SurveySerilaizer, AppSurveyQuestionSerilizer
from e_learning.models import Kiosk_E_Learning, App_Survey , SurveyQA, AppSurveyQuestion, AppSurveyQuestion


class Kiosk_E_Learning_View (ListAPIView):
    permission_classes = [IsAuthenticated ,KOKPermission, KOKMerchantPermission]
    serializer_class = E_LearningSerializer
    queryset = Kiosk_E_Learning.objects.all()

    def list (self, request, *args, **kwargs):
        e_learning = self.get_queryset().filter( e_leanring_country = request.user.country_of_residence )
        serializer = self.serializer_class (e_learning , many=True)
        return Response({'status':'success', 'message':'list of all kiosk E learning', 'data':serializer.data}, status=status.HTTP_200_OK)
    


class ListSurveyQuestions(ListAPIView):
    permission_classes = [ KOKPermission , IsAuthenticated,]
    queryset = AppSurveyQuestion.objects.all()
    serializer_class = AppSurveyQuestionSerilizer


class AppSubmiSurvey(ListCreateAPIView):
    permission_classes =  [ KOKPermission , IsAuthenticated, KOKMerchantOnly]
    # queryset = App_Survey.objects.all()
    serializer_class = App_SurveySerilaizer

    def list (self,request, *args, **kwargs):
        qs = App_Survey.objects.all().filter( user = self.request.user )
        serializer = self.get_serializer(qs, many= True)
        return Response( serializer.data )
    
    def create (self,request, *args, **kwargs):
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            survey_qas = serializer.validated_data.pop('survey_qa')
            # confirmation of the product is been created
            for survey_QA in survey_qas:
                if survey_QA.get("survey_questions_id" ) is not None:
                    user_acc = App_Survey()
                    user_acc.user = self.request.user
                    user_acc.save()
                    ques_id = survey_QA.get("survey_questions_id")
                    # getting the question instance
                    try:
                        ques_qs =  AppSurveyQuestion.objects.get(survey_question = ques_id)
                    except AppSurveyQuestion.DoesNotExist:
                        return Response({'status':'error','message':'question id does not exist'} )
                    SurveyQA.objects.create(
                        survey_questions_id = ques_qs ,
                        survey_answer = survey_QA.get("survey_answer" ), 
                        survey_qa = user_acc 
                        )
                

                        
            return Response({'status':'successful','message':'app survey is submitted successful'} )
            
            


    