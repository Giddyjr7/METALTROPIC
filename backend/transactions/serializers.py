from rest_framework import serializers
from .models import TransactionHistory


class TransactionHistorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    transaction_type_display = serializers.CharField(source="get_transaction_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = TransactionHistory
        fields = [
            'id',
            'username',
            'reference',
            'transaction_type',
            'transaction_type_display',
            'amount',
            'description',
            'status',
            'status_display',
            'balance_before',
            'balance_after',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'username',
            'reference',
            'transaction_type_display',
            'status_display',
            'balance_before',
            'balance_after',
            'created_at',
        ]
