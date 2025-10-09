from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import InvestmentPlan, UserInvestment
from .serializers import InvestmentPlanSerializer, UserInvestmentSerializer


def index(request):
    return JsonResponse({"message": "Investments API is working!"})


class InvestmentPlanListView(generics.ListAPIView):
    """
    List all available investment plans.
    """
    queryset = InvestmentPlan.objects.all()
    serializer_class = InvestmentPlanSerializer
    permission_classes = [permissions.AllowAny]


class StartInvestmentView(generics.CreateAPIView):
    """
    Start a new investment for logged-in user.
    """
    serializer_class = UserInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
