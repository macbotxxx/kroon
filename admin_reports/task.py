from notifications.mobile_notification import *
from kroon.users.models import User


@celery_app.task()
def device_push_notification( *args , **kwargs ):
    serializer = kwargs.pop('serializer', None)
    title = serializer.validated_data['title']
    body_message = serializer.validated_data['body_message']
    platform = serializer.validated_data['platform']
    news_feed_country = serializer.validated_data['news_feed_country']
    notification_type = "newsfeed"
    for i in news_feed_country:
        user_device = User.objects.select_related('country_of_residence','country_province','on_boarding_user','government_organization_name','government_organization_name').filter( country_of_residence = i )
        for device_id in user_device:
            mobile_push_notification.delay(
                title = title,
                body_message = body_message,
                platform = platform.lower(),
                device_id = device_id.device_id,
                notification_type = notification_type
            )
    
    return "Admin push notification is sent out"



