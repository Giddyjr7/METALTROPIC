from django.urls import path
from .views import (
    # 📈 Investment Views
    InvestmentPlanListView,
    StartInvestmentView,
    UserInvestmentListView,
    UserInvestmentDetailView,
    InvestmentProfitView,
    ActiveInvestmentsView,
    CompleteExpiredInvestmentsView,

    # 💰 Deposit Views
    DepositCreateView,
    DepositListView,
    ApproveDepositView,

    # 💸 Withdrawal Views
    WithdrawalCreateView,
    WithdrawalListView,
    ApproveWithdrawalView,

    # 👛 Wallet View
    WalletView,
)

urlpatterns = [
    # ==========================
    # 📈 INVESTMENT ROUTES
    # ==========================
    path('plans/', InvestmentPlanListView.as_view(), name='investment-plans'),             # List all investment plans
    path('start/', StartInvestmentView.as_view(), name='start-investment'),                # Start a new investment
    path('my/', UserInvestmentListView.as_view(), name='my-investments'),                  # View user’s investments
    path('my/<int:pk>/', UserInvestmentDetailView.as_view(), name='investment-detail'),    # View single investment details
    path('my/<int:pk>/profit/', InvestmentProfitView.as_view(), name='investment-profit'), # Check profit on investment
    path('active/', ActiveInvestmentsView.as_view(), name='active-investments'),           # View all active investments
    path('complete-expired/', CompleteExpiredInvestmentsView.as_view(), name='complete-expired'),  # Admin: complete expired investments

    # ==========================
    # 💰 DEPOSIT ROUTES
    # ==========================
    path('deposit/', DepositCreateView.as_view(), name='create-deposit'),                  # User uploads deposit proof
    path('deposits/', DepositListView.as_view(), name='list-deposits'),                    # Admin: view all deposits
    path('approve-deposit/<int:pk>/', ApproveDepositView.as_view(), name='approve-deposit'),  # Admin: approve/reject deposit

    # ==========================
    # 💸 WITHDRAWAL ROUTES
    # ==========================
    path('withdraw/', WithdrawalCreateView.as_view(), name='create-withdrawal'),           # User requests withdrawal
    path('withdrawals/', WithdrawalListView.as_view(), name='list-withdrawals'),           # Admin: view all withdrawals
    path('approve-withdrawal/<int:pk>/', ApproveWithdrawalView.as_view(), name='approve-withdrawal'),  # Admin: approve/reject withdrawal

    # ==========================
    # 👛 WALLET ROUTE
    # ==========================
    path('wallet/', WalletView.as_view(), name='user-wallet'),                             # View user’s wallet balance
]
