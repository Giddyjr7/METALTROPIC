from rest_framework import serializers
from .models import (
    InvestmentPlan,
    UserInvestment,
    Deposit,
    Withdrawal,
)
from wallets.models import Wallet


# ==========================
# 📈 INVESTMENT SERIALIZERS
# ==========================

class InvestmentPlanSerializer(serializers.ModelSerializer):
    """Serializer for listing available investment plans."""
    class Meta:
        model = InvestmentPlan
        fields = '__all__'


class UserInvestmentSerializer(serializers.ModelSerializer):
    """Serializer for creating and viewing user investments."""
    plan_name = serializers.CharField(source='plan.name', read_only=True)

    class Meta:
        model = UserInvestment
        fields = [
            'id', 'user', 'plan', 'plan_name', 'amount', 'start_date', 'end_date',
            'status', 'expected_profit', 'total_payout'
        ]
        read_only_fields = ['user', 'start_date', 'end_date', 'status', 'expected_profit', 'total_payout']

    def create(self, validated_data):
        user = self.context['request'].user
        plan = validated_data['plan']
        amount = validated_data['amount']

        # ✅ Validate amount range
        if not (plan.min_amount <= amount <= plan.max_amount):
            raise serializers.ValidationError({
                "amount": f"Amount must be between ₦{plan.min_amount} and ₦{plan.max_amount}"
            })

        # ✅ Check user wallet balance
        wallet = getattr(user, 'wallet', None)
        if not wallet or wallet.balance < amount:
            raise serializers.ValidationError({"error": "Insufficient wallet balance."})

        # ✅ Debit user wallet
        wallet.debit(amount)

        # ✅ Calculate expected profit
        investment = UserInvestment.objects.create(
            user=user,
            plan=plan,
            amount=amount,
            expected_profit=0,
        )
        investment.calculate_expected_profit()
        investment.save()
        return investment


class InvestmentProfitSerializer(serializers.ModelSerializer):
    """Serializer for showing investment profit."""
    plan_name = serializers.CharField(source='plan.name', read_only=True)

    class Meta:
        model = UserInvestment
        fields = ['id', 'plan_name', 'amount', 'expected_profit', 'status', 'total_payout']


# ==========================
# 💰 DEPOSIT SERIALIZERS
# ==========================

class DepositSerializer(serializers.ModelSerializer):
    """Serializer for user deposit creation and viewing."""
    class Meta:
        model = Deposit
        fields = ['id', 'user', 'amount', 'proof', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']


class DepositApprovalSerializer(serializers.ModelSerializer):
    """Admin serializer for approving/rejecting deposits."""
    class Meta:
        model = Deposit
        fields = ['id', 'status']

    def update(self, instance, validated_data):
        status_choice = validated_data.get('status')
        if status_choice == 'approved':
            instance.approve()
        elif status_choice == 'rejected':
            instance.reject()
        else:
            raise serializers.ValidationError({"status": "Invalid status option."})
        return instance


# ==========================
# 💸 WITHDRAWAL SERIALIZERS
# ==========================

class WithdrawalSerializer(serializers.ModelSerializer):
    """Serializer for user withdrawals."""
    class Meta:
        model = Withdrawal
        fields = ['id', 'user', 'amount', 'wallet_address', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        wallet = getattr(user, 'wallet', None)
        amount = validated_data.get("amount")

        if not wallet or wallet.balance < amount:
            raise serializers.ValidationError({"error": "Insufficient wallet balance."})

        withdrawal = Withdrawal.objects.create(user=user, **validated_data)
        return withdrawal



class WithdrawalApprovalSerializer(serializers.ModelSerializer):
    """Admin serializer for approving/rejecting withdrawals."""
    class Meta:
        model = Withdrawal
        fields = ['id', 'status']

    def update(self, instance, validated_data):
        status_choice = validated_data.get('status')
        if status_choice == 'approved':
            instance.approve()
        elif status_choice == 'rejected':
            instance.reject()
        else:
            raise serializers.ValidationError({"status": "Invalid status option."})
        return instance


# ==========================
# 👛 WALLET SERIALIZER
# ==========================

class WalletSerializer(serializers.ModelSerializer):
    """Serializer for displaying wallet balance."""
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'last_updated']
        read_only_fields = ['user', 'balance', 'last_updated']
        
