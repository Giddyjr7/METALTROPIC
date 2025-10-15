from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import TransactionHistory
from .serializers import TransactionHistorySerializer


class TransactionHistoryListView(generics.ListAPIView):
    """
    🔹 Returns all transactions for the logged-in user.
    🔹 Supports filtering by:
         - ?type=deposit
         - ?status=successful
         - ?search=reference (search by reference ID)
    🔹 Admin users can view all users’ transactions.
    """
    serializer_class = TransactionHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['reference']

    def get_queryset(self):
        user = self.request.user

        # Admins can view all users' transactions
        if user.is_staff or user.is_superuser:
            queryset = TransactionHistory.objects.all().order_by('-created_at')
        else:
            queryset = TransactionHistory.objects.filter(user=user).order_by('-created_at')

        # Optional filter by transaction type (deposit, withdrawal, profit, etc.)
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        # Optional filter by status (successful, pending, failed)
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset
