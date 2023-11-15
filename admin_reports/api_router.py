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
    CategorySales,
    BusinessRecords
    )

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


router.register("transactions", TransactionListView, basename="all_transactions")
router.register("users-list", AllUserListView, basename="user_list")
router.register("total-transactions", TotalTransactions, basename="total_transactions")
router.register("total-wallet-value", TotalWalletValue, basename="total_wallet_value")
router.register("total-payouts", TotalPayouts, basename="total_payouts")
router.register("total-e-wallets", TotalEwallets, basename="total_e_wallets")
router.register("total-merchants", TotalMerchants, basename="total_merchants")
router.register("cross-border-transfers", CrossBorderTransfer, basename="cross_border_transfers")
router.register("daily-average", DailyAverage, basename="daily_average")
router.register("active-merchants", TotalActiveMerchants, basename="active_merchants")
router.register("global-overview", GlobalOverview, basename="global_overview")
router.register("news-feed", NewsFeedViewSet, basename="news_feed")
router.register("e-learning", ELearningViewSet, basename="e_learning")
router.register("survey", SurveyViewSet, basename="survey")
router.register("answered-survey", AnsweredSurveyViewSet, basename="answered_survey")
router.register("inapp-ad", InAppAdsViewSet, basename="inapp_ad")
router.register("global-sales", GlobalSales, basename="global_sales")
router.register("transaction-channel", TransactionChannels, basename="transaction_channel")
router.register("category-sales", CategorySales, basename="category_sales")
router.register("business-records", BusinessRecords, basename="business_records")

app_name = "admin_reports"
urlpatterns = router.urls
