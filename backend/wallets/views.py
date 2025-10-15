from rest_framework import generics, permissions
from .models import Wallet
from .serializers import WalletSerializer

class WalletDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WalletSerializer

    def get_object(self):
        return self.request.user.wallet
