from django.urls import path
from . import views


urlpatterns = [

    path('list-of-sales/', views.List_Of_Sales_Views.as_view(), name='list_of_sales'),
    path('my-report/', views.Sales_Report.as_view(), name='total_sales'),
    path('sale-details/<str:order_id>/', views.Sale_detailsView.as_view(), name='sales_details'),
    path('business-financial-reports/', views.Business_Financial_Reports.as_view(), name="business_financial_reports"),
    path('product-refund/<str:order_id>/<str:product_sku>/<str:product_quantity>/', views.Refund_Product.as_view(), name='product_refund'),
    path('order-refund/<str:order_id>/', views.Refund_Order.as_view(), name='order_refund'),
]