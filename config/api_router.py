from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from admin_reports.api.views import (
    TransactionListView, 
    AllUserListView)

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


router.register("transactions", TransactionListView)
router.register("users-list", AllUserListView)

app_name = "admin_reports"
urlpatterns = router.urls
