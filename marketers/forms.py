from django import forms
from django.utils.translation import gettext_lazy as _

from locations.models import Country
from ads.models import Ads
from notifications.models import NewsFeed



class General_Push_Notification_Mobile (forms.Form):
    title = forms.CharField(max_length=30)
    message = forms.CharField(max_length=178)

    def __init__(self, *args, **kwargs):
        super(General_Push_Notification_Mobile, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = _('Push mobile notification title')
        self.fields['message'].widget.attrs['placeholder'] = _('type your push notification message')
       
        self.fields['title'].help_text = _('this represents a push notification title that will be displayed to the user mobile device header.')
        self.fields['message'].help_text = _('the push notification message is also known as the push notification content , NOTE its should be more than 178 characters long for better understanding.')


class General_Push_Notification_Mobile_Per_Country (forms.Form):
    country = forms.ModelMultipleChoiceField(
        queryset=Country.objects.filter(accept_signup=True).order_by('name'),
        # empty_label=_('Country of Residence'),
        help_text=_('this shows the countries that is valid for kroon'))
    title = forms.CharField(max_length=30)
    message = forms.CharField(max_length=178)

    def __init__(self, *args, **kwargs):
        super(General_Push_Notification_Mobile_Per_Country, self).__init__(*args, **kwargs)
        self.fields['country'].widget.attrs['placeholder'] = _('select country')
        self.fields['title'].widget.attrs['placeholder'] = _('Push mobile notification title')
        self.fields['message'].widget.attrs['placeholder'] = _('type your push notification message')
       
        self.fields['title'].help_text = _('this represents a push notification title that will be displayed to the user mobile device header.')
        self.fields['message'].help_text = _('the push notification message is also known as the push notification content , NOTE its should be more than 178 characters long for better understanding.')



class Email_Notification (forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','type':'text'}))
    header = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','type':'text'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','id':'summernote'}))


    def __init__(self, *args, **kwargs):
        super(Email_Notification, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['placeholder'] = _('type email subject')
        self.fields['header'].widget.attrs['placeholder'] = _('type email header')
        self.fields['header'].widget.attrs['value'] = _('Input Email Header Here.')
        
        self.fields['subject'].help_text = _('this represents a email subject that will be displayed on the outer layer of the email.')
        self.fields['header'].help_text = _('this represents a email notification title that will be displayed as a title to the user.')
        self.fields['content'].help_text = _('The email notification content hsould contain the message that is meant to be sent to the user.')


class Email_Notification_Per_Country (forms.Form):
    country = forms.ModelMultipleChoiceField(
        queryset=Country.objects.filter(accept_signup=True).order_by('name'),
        # empty_label=_('Country of Residence'),
        help_text=_('this shows the countries that is valid for kroon'))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','type':'text'}))
    header = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','type':'text'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','id':'summernote'}))


    def __init__(self, *args, **kwargs):
        super(Email_Notification_Per_Country, self).__init__(*args, **kwargs)
        self.fields['country'].widget.attrs['placeholder'] = _('select country')
        self.fields['subject'].widget.attrs['placeholder'] = _('type email subject')
        self.fields['header'].widget.attrs['placeholder'] = _('type email header')
        self.fields['header'].widget.attrs['value'] = _('Input Email Header Here.')
        
        self.fields['subject'].help_text = _('this represents a email subject that will be displayed on the outer layer of the email.')
        self.fields['header'].help_text = _('this represents a email notification title that will be displayed as a title to the user.')
        self.fields['content'].help_text = _('The email notification content hsould contain the message that is meant to be sent to the user.')


class general_ad_form (forms.ModelForm):
    ad_url = forms.CharField(required=False)
    active = forms.BooleanField(required = True)

    class Meta:
        model = Ads
        fields = ('ad_country', 'ad_name', 'ad_image', 'ad_url', 'platform','active', )



class general_news_feed (forms.ModelForm):
    status = forms.BooleanField(required = True)
    class Meta:
        model = NewsFeed
        fields = ('title', 'image', 'content', 'news_feed_country', 'status')