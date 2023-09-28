from django import forms
from .models import Onboarding_Users_CSV
from ads.models import Ads
from notifications.models import NewsFeed


class Onboarding_Users_Form(forms.ModelForm):

    class Meta:
        model = Onboarding_Users_CSV
        fields = ['on_boarding_user_file']



class Push_Notifications_Form(forms.ModelForm):

    class Meta:
        model = Ads
        fields = ['ad_name', 'ad_image', 'ad_url']



class Publish_NewsFeed_Form(forms.ModelForm):

    class Meta:
        model = NewsFeed
        fields = ['title', 'image', 'content',]

