from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from notifications.api.views import (
    GeneralNotificationViewSet, 
   
    )

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


router.register("general-push-notification", GeneralNotificationViewSet, basename="push-notification")


app_name = "notifications"
urlpatterns = router.urls
