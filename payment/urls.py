from django.urls import path, include
from rest_framework import routers

from payment.views import BalanceViewSet, TransactionViewSet

app_name = "payments"

router = routers.DefaultRouter()
router.register("balances", BalanceViewSet)
router.register("transactions", TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
