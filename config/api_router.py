from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from admin_reports.api.views import (
    TransactionListView
    )

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


router.register("transactions", TransactionListView)

app_name = "api"
urlpatterns = router.urls
