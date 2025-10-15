from django.contrib import admin
from .models import TransactionHistory


@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'transaction_type',
        'amount',
        'status',
        'balance_before',
        'balance_after',
        'reference',
        'created_at',
    )
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('user__username', 'reference', 'description')
    ordering = ('-created_at',)
    readonly_fields = (
        'user',
        'transaction_type',
        'amount',
        'fee',
        'balance_before',
        'balance_after',
        'status',
        'reference',
        'description',
        'created_at',
    )

    list_per_page = 25
    date_hierarchy = 'created_at'
    save_on_top = True
