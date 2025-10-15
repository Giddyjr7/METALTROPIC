from django.contrib import admin
from .models import Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'total_invested', 'total_withdrawn', 'created_at')
    search_fields = ('user__username',)
