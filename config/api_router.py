from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from admin_reports.api.views import (
    TransactionListView, 
    AllUserListView,
    TotalTransactions,
    TotalWalletValue,
    TotalPayouts,
    TotalEwallets,
    TotalMerchants,
    CrossBorderTransfer,
    DailyAverage,
    TotalActiveMerchants,
    TopPerformingRegions,
    GlobalOverview
    )

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


router.register("transactions", TransactionListView)
router.register("users-list", AllUserListView)
router.register("total-transactions", TotalTransactions)
router.register("total-wallet-value", TotalWalletValue)
router.register("total-payouts", TotalPayouts)
router.register("total-e-wallets", TotalEwallets)
router.register("total-merchants", TotalMerchants)
router.register("cross-border-transfers", CrossBorderTransfer)
router.register("daily-average", DailyAverage)
router.register("active-merchants", TotalActiveMerchants)
router.register("top-performing-regions", TopPerformingRegions)
router.register("global_overview", GlobalOverview)

app_name = "admin_reports"
urlpatterns = router.urls
