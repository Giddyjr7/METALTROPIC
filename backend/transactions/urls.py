from django.urls import path
from .views import TransactionHistoryListView

urlpatterns = [
    path('', TransactionHistoryListView.as_view(), name='transaction-history'),
]
