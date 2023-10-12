from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from locations.models import Country
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.


class Kiosk_E_Learning (BaseModel):
    """E-Learning mmodel section """

    title = models.CharField(
        verbose_name = _('Kiosk E-Learning'),
        max_length =255,
        null=True, blank=True,
        help_text = _('This hold the e-learning title of this particular Kiosk E-Learning.')
    )

    vd_thumbnail = models.ImageField(
        verbose_name = _('E-Learning video thumbnail'),
        null =True, blank=True,
        help_text = _('this holds the e-leanry video thumbnail for the particular learning vd')
    )

    vd_link = models.URLField(
        verbose_name = _('E Learning Video Link'),
        null=True, blank=True,
        help_text = _('This section represents the video link for the E-Learning video')
    )

    duration = models.CharField(
        verbose_name = _('Video Duration'),
        max_length =255,
        null=True, blank=True,
        help_text = _('This hold the current video duration of the e-Learning process.')
    )

    e_leanring_country = models.ManyToManyField(
        Country,
        help_text = _(" this is the country that will be able to see this ad image")
    )

    
    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Kiosk E-Learning')
        verbose_name_plural = _('Kiosk E-Learning')
        # icon = _("mcihiasnanaisna")



class App_Survey ( BaseModel ):
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        related_name="merchant_survey",
        blank=True,
        help_text=_("The user for whom account belongs to")
    )

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Merchant Survey")
        verbose_name_plural = _("Merchant Surveys")

    def __str__(self):
        return str(self.user)
    

class AppSurveyQuestion(BaseModel):

    survey_question = models.CharField(
        verbose_name = _('Survey Questions'),
        max_length = 300,
        null=True,blank=True,
        help_text = _("this shows rthe question of the survey")
    )

    class Meta:
        verbose_name = _("App Survey Question")
        verbose_name_plural = _("App Surveys Question")

    def __str__(self):
        return str(self.survey_question) 


class SurveyQA(BaseModel):
    """
    this holds the survey question and answers
    """
    # registering custom manager interface

    survey_qa = models.ForeignKey(
        App_Survey, on_delete=models.SET_NULL,
        null=True,
        related_name='survey_user',
        verbose_name = _('User Account'),
        help_text = _('this hold the user account that answered the survey questions')
    )

    survey_questions_id = models.ForeignKey(
        AppSurveyQuestion, on_delete=models.CASCADE,
        null=True,
        related_name='survey_field',
        verbose_name = _('Survey QA'),
        help_text = _('this hold the survey question ')
    )

    survey_answer = models.CharField(
        verbose_name = _('Survey Answer'),
        null =True,
        max_length = 300, blank=True,
        help_text=_("the hold the answer of the survey")
    )

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Survey Q and A ")
        verbose_name_plural = _("Survey Q and A")

    def __str__(self):
        return str(self.survey_qa)


    