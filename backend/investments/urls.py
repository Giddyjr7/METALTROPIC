# from django.urls import path
# from .views import InvestmentPlanListView, StartInvestmentView, MyInvestmentsView, CalculateROIView
# from . import views


# urlpatterns = [
#     # path('', views.index, name='investments-index'),
#     path("plans/", InvestmentPlanListView.as_view(), name="investment-plans"),
#     path("start/", StartInvestmentView.as_view(), name="start-investment"),
#     path('my-investments/', MyInvestmentsView.as_view(), name='my-investments'),
#     path('calculate-roi/', CalculateROIView.as_view(), name='calculate-roi'),
#      path('my-investments/', views.my_investments, name='my-investments'),
#     path('update-profits/', views.update_profits, name='update-profits'),
# ]

from django.urls import path
from .views import (
    InvestmentPlanListView,
    StartInvestmentView,
    UserInvestmentListView,
    UserInvestmentDetailView,
    InvestmentProfitView,
    ActiveInvestmentsView,
    CompleteExpiredInvestmentsView,
    DepositCreateView,
    DepositListView,
    WithdrawalCreateView,
    WithdrawalListView,
    WalletView
)

urlpatterns = [
    path('plans/', InvestmentPlanListView.as_view(), name='investment-plans'),
    path('start/', StartInvestmentView.as_view(), name='start-investment'),
    path('my/', UserInvestmentListView.as_view(), name='my-investments'),
    path('my/<int:pk>/', UserInvestmentDetailView.as_view(), name='investment-detail'),
    path('my/<int:pk>/profit/', InvestmentProfitView.as_view(), name='investment-profit'),
    path('active/', ActiveInvestmentsView.as_view(), name='active-investments'),
    path('complete-expired/', CompleteExpiredInvestmentsView.as_view(), name='complete-expired'),
    # Deposit & Withdrawal Routes
    path('deposit/', DepositCreateView.as_view(), name='create-deposit'),
    path('deposits/', DepositListView.as_view(), name='list-deposits'),
    path('withdraw/', WithdrawalCreateView.as_view(), name='create-withdrawal'),
    path('withdrawals/', WithdrawalListView.as_view(), name='list-withdrawals'),
    path('wallet/', WalletView.as_view(), name='user-wallet'),
]


