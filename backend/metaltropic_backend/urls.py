
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App routes (we’ll add later)
    path('api/accounts/', include('accounts.urls')),
    path('api/investments/', include('investments.urls')),
    path('api/transactions/', include('transactions.urls')),
    path('api-auth/', include('rest_framework.urls')),


    path("", lambda request: JsonResponse({"status": "ok", "message": "Welcome to the MetalTropic API"})),
]
