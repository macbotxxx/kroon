from notifications.mobile_notification import *
from kroon.users.models import User


@celery_app.task()
def device_push_notification( *args , **kwargs ):
    serializer = kwargs.pop('serializer', None)
    title = serializer.validated_data['title']
    body_message = serializer.validated_data['body_message']
    platform = serializer.validated_data['platform']
    news_feed_country = serializer.validated_data['news_feed_country']
    for i in news_feed_country:
        pass
    return "Admin push notification is sent out"



