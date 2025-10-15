from django.contrib import admin
from .models import (
    InvestmentPlan,
    UserInvestment,
    Deposit,
    Withdrawal,
)



# ==============================
# 📈 Investment Models
# ==============================
@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_amount', 'max_amount', 'daily_roi', 'duration_days', 'total_return')
    search_fields = ('name',)
    list_filter = ('duration_days', 'compound_interest')
    ordering = ('-daily_roi',)


@admin.register(UserInvestment)
class UserInvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'status', 'start_date', 'end_date', 'expected_profit', 'total_payout')
    list_filter = ('status', 'plan')
    search_fields = ('user__username', 'plan__name')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)



@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
# Note: Consider adding actions for bulk approving/rejecting deposits and withdrawals in the future.
# ==============================
# 🧩 Developer Note
# ==============================
# Note: Consider adding admin actions for bulk approving/rejecting
# deposits and withdrawals in the future. This can streamline
# admin workflow and reduce manual review time.