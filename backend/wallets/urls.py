from django.urls import path
from .views import WalletDetailView

urlpatterns = [
    path('', WalletDetailView.as_view(), name='wallet-detail'),
]
