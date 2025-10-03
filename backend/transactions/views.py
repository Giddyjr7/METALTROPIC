from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def index(request):
    return JsonResponse({"message": "Transactions API is working!"})

