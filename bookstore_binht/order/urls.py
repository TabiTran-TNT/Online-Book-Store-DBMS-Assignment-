from django.urls import path

from .views import (
    CheckoutView,
    PastOrderListView,
    PaymentView,
    cash_payment,
    payment_status,
)

app_name = "order"

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("payment/", PaymentView.as_view(), name="order_payment"),
    path("payment-status/", payment_status, name="payment_status"),
    path("cash-payment/", cash_payment, name="cash_payment"),
    path("history/", PastOrderListView.as_view(), name="order_history"),
]
