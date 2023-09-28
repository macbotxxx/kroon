from rest_framework import serializers
from e_learning.models import Kiosk_E_Learning, App_Survey , SurveyQA , AppSurveyQuestion


class E_LearningSerializer (serializers.ModelSerializer):

    class Meta:
        model = Kiosk_E_Learning
        fields = ('title','vd_thumbnail', 'vd_link', 'duration')
        

class AppSurveyQuestionSerilizer(serializers.ModelSerializer):
    class Meta:
        model = AppSurveyQuestion
        fields = ('id','survey_question',)



class SurveyQASerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQA
        fields = ('survey_questions_id', 'survey_answer',)


class App_SurveySerilaizer (serializers.ModelSerializer):
    survey_qa = SurveyQASerializer( many = True ,  required = False)
    class Meta:
        model = App_Survey
        fields = ['user', 'survey_qa']
        read_only_fields = ('user',)