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
    GlobalOverview,
    NewsFeedViewSet,
    ELearningViewSet,
    SurveyViewSet,
    AnsweredSurveyViewSet,
    InAppAdsViewSet,
    GlobalSales,
    TransactionChannels,
    CategorySales
    )

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


router.register("transactions", TransactionListView, basename="all_transactions")
router.register("users-list", AllUserListView)
router.register("total-transactions", TotalTransactions)
router.register("total-wallet-value", TotalWalletValue)
router.register("total-payouts", TotalPayouts)
router.register("total-e-wallets", TotalEwallets)
router.register("total-merchants", TotalMerchants)
router.register("cross-border-transfers", CrossBorderTransfer)
router.register("daily-average", DailyAverage)
router.register("active-merchants", TotalActiveMerchants)
router.register("global_overview", GlobalOverview)
router.register("news-feed", NewsFeedViewSet)
router.register("e-learning", ELearningViewSet)
router.register("survey", SurveyViewSet)
router.register("answered-survey", AnsweredSurveyViewSet)
router.register("inapp-ad", InAppAdsViewSet)
router.register("global-sales", GlobalSales)
router.register("transaction-channel", TransactionChannels)
router.register("category-sales", CategorySales)

app_name = "admin_reports"
urlpatterns = router.urls
