from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import InvestmentPlan, UserInvestment, Investment, Deposit, Withdrawal, UserWallet
from .serializers import (
    InvestmentPlanSerializer,
    UserInvestmentSerializer,
    InvestmentSerializer,
    InvestmentProfitSerializer,
    DepositSerializer, 
    WithdrawalSerializer,
    WalletSerializer
)
from django.utils import timezone


# ✅ Get all investment plans
class InvestmentPlanListView(generics.ListAPIView):
    queryset = InvestmentPlan.objects.all()
    serializer_class = InvestmentPlanSerializer
    permission_classes = [permissions.AllowAny]


# ✅ View all user investments
class UserInvestmentListView(generics.ListAPIView):
    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInvestment.objects.filter(user=self.request.user).order_by("-start_date")


# ✅ Start a new investment
class StartInvestmentView(generics.CreateAPIView):
    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ✅ Get a single investment detail
class UserInvestmentDetailView(generics.RetrieveAPIView):
    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInvestment.objects.filter(user=self.request.user)


# ✅ Track investment progress (profit, total return)
class InvestmentProfitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            investment = UserInvestment.objects.get(pk=pk, user=request.user)
        except UserInvestment.DoesNotExist:
            return Response(
                {"error": "Investment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = InvestmentProfitSerializer(investment)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ✅ View all active investments
class ActiveInvestmentsView(generics.ListAPIView):
    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInvestment.objects.filter(
            user=self.request.user, status="active"
        ).order_by("-start_date")


# ✅ Automatically complete expired investments (optional cron or manual endpoint)
class CompleteExpiredInvestmentsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        now = timezone.now()
        expired_investments = UserInvestment.objects.filter(
            end_date__lt=now, status="active"
        )

        count = expired_investments.update(status="completed")
        return Response(
            {"message": f"{count} investment(s) marked as completed."},
            status=status.HTTP_200_OK,
        )
    

# Deposit and Withdrawal Views
class DepositCreateView(generics.CreateAPIView):
    """
    User uploads payment proof for deposit.
    """
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepositListView(generics.ListAPIView):
    """
    Admin can view all deposits.
    """
    queryset = Deposit.objects.all().order_by('-created_at')
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAdminUser]


class WithdrawalCreateView(generics.CreateAPIView):
    """
    User requests withdrawal to crypto wallet.
    """
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]


class WithdrawalListView(generics.ListAPIView):
    """
    Admin can view all withdrawal requests.
    """
    queryset = Withdrawal.objects.all().order_by('-created_at')
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAdminUser]


# User Wallet View
class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, _ = UserWallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)