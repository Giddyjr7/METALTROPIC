from django.urls import path
from .views import InvestmentPlanListView, StartInvestmentView


urlpatterns = [
    # path('', views.index, name='investments-index'),
    path("plans/", InvestmentPlanListView.as_view(), name="investment-plans"),
    path("start/", StartInvestmentView.as_view(), name="start-investment")
]

# from django.urls import path
# from .views import InvestmentPlanListView, StartInvestmentView

# urlpatterns = [
#     path("plans/", InvestmentPlanListView.as_view(), name="investment-plans"),
#     path("start/", StartInvestmentView.as_view(), name="start-investment"),
# ]

