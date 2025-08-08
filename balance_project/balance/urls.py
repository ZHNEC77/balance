from django.urls import path
from .views import (
    BalanceView,
    DepositView,
    TransferView,
    TransactionHistoryView,
)

urlpatterns = [
    path('', BalanceView.as_view(), name='balance'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('transactions/', TransactionHistoryView.as_view(), name='transactions'),
]
