from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from django.db import models
from django.utils import timezone
from transactions.models import TransactionHistory
from .models import (
    InvestmentPlan,
    UserInvestment,
    Deposit,
    Withdrawal,
)
from wallets.models import Wallet  # ✅ Correct wallet import

from .serializers import (
    InvestmentPlanSerializer,
    UserInvestmentSerializer,
    InvestmentProfitSerializer,
    DepositSerializer,
    WithdrawalSerializer,
    WalletSerializer,
    DepositApprovalSerializer,
    WithdrawalApprovalSerializer
)


# ==========================
# 📈 INVESTMENT VIEWS
# ==========================

class InvestmentPlanListView(generics.ListAPIView):
    """List all available investment plans."""
    queryset = InvestmentPlan.objects.all()
    serializer_class = InvestmentPlanSerializer
    permission_classes = [permissions.AllowAny]


class UserInvestmentListView(generics.ListAPIView):
    """List all investments by the authenticated user."""
    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInvestment.objects.filter(user=self.request.user).order_by("-start_date")


class StartInvestmentView(generics.CreateAPIView):
    """Start a new investment."""
    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserInvestmentDetailView(generics.RetrieveAPIView):
    """Get a single investment detail."""
    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInvestment.objects.filter(user=self.request.user)


class InvestmentProfitView(APIView):
    """View investment profit & status."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            investment = UserInvestment.objects.get(pk=pk, user=request.user)
        except UserInvestment.DoesNotExist:
            return Response({"error": "Investment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InvestmentProfitSerializer(investment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActiveInvestmentsView(generics.ListAPIView):
    """List active investments."""
    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInvestment.objects.filter(user=self.request.user, status="active").order_by("-start_date")


class CompleteExpiredInvestmentsView(APIView):
    """Admin: Automatically complete expired investments."""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        now = timezone.now()
        expired_investments = UserInvestment.objects.filter(end_date__lt=now, status="active")
        count = expired_investments.update(status="completed")
        return Response({"message": f"{count} investment(s) marked as completed."}, status=status.HTTP_200_OK)


# ==========================
# 💰 DEPOSIT VIEWS
# ==========================

class DepositCreateView(generics.CreateAPIView):
    """User uploads payment proof for deposit."""
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status="pending")


class DepositListView(generics.ListAPIView):
    """Admin: View all deposits."""
    queryset = Deposit.objects.all().order_by('-created_at')
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAdminUser]


class ApproveDepositView(generics.UpdateAPIView):
    """Admin approves or rejects a deposit."""
    queryset = Deposit.objects.all()
    serializer_class = DepositApprovalSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 💵 Update wallet if approved
        if instance.status == "approved":
            wallet, _ = Wallet.objects.get_or_create(user=instance.user)
            wallet.balance += instance.amount
            wallet.save()

        return Response({"message": f"Deposit {instance.status} successfully."}, status=status.HTTP_200_OK)


# ==========================
# 💸 WITHDRAWAL VIEWS
# ==========================

class WithdrawalCreateView(generics.CreateAPIView):
    """User requests a withdrawal."""
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        amount = serializer.validated_data.get("amount")

        if wallet.balance < amount:
            raise ValidationError({"error": "Insufficient funds."})

        serializer.save(user=self.request.user, status="pending")


class WithdrawalListView(generics.ListAPIView):
    """Admin: View all withdrawal requests."""
    queryset = Withdrawal.objects.all().order_by('-created_at')
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAdminUser]


class ApproveWithdrawalView(generics.UpdateAPIView):
    """Admin approves or rejects a withdrawal."""
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalApprovalSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 💸 Update wallet if approved
        if instance.status == "approved":
            wallet, _ = Wallet.objects.get_or_create(user=instance.user)
            if wallet.balance >= instance.amount:
                wallet.balance -= instance.amount
                wallet.save()
            else:
                return Response({"error": "Insufficient wallet balance."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"Withdrawal {instance.status} successfully."}, status=status.HTTP_200_OK)


# ==========================
# 👛 WALLET VIEWS
# ==========================

class WalletView(APIView):
    """Get current wallet balance."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ==========================
# 📊 DASHBOARD OVERVIEW VIEW
# ==========================

class WalletOverviewView(APIView):
    """Provides full dashboard summary for Overview tab."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        wallet, _ = Wallet.objects.get_or_create(user=user)

        total_deposits = (
            Deposit.objects.filter(user=user, status="approved")
            .aggregate(total=models.Sum("amount"))
            .get("total") or Decimal("0.00")
        )

        total_withdrawals = (
            Withdrawal.objects.filter(user=user, status="approved")
            .aggregate(total=models.Sum("amount"))
            .get("total") or Decimal("0.00")
        )

        total_profits = (
            UserInvestment.objects.filter(user=user, status="completed")
            .aggregate(total=models.Sum("expected_profit"))
            .get("total") or Decimal("0.00")
        )

        last_txn = (
            TransactionHistory.objects.filter(user=user)
            .order_by("-created_at")
            .first()
        )

        last_transaction_data = (
            {
                "transaction_type": last_txn.transaction_type,
                "amount": last_txn.amount,
                "status": last_txn.status,
                "created_at": last_txn.created_at,
            }
            if last_txn
            else None
        )

        data = {
            "balance": wallet.balance,
            "total_deposits": total_deposits,
            "total_withdrawals": total_withdrawals,
            "total_profits": total_profits,
            "last_transaction": last_transaction_data,
        }

        return Response(data, status=status.HTTP_200_OK)
