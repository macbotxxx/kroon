from rest_framework import serializers
from notifications.models import NewsFeed

class NewsFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsFeed
        fields = ['id','title', 'image', 'content','created_date']
       


        