from rest_framework import serializers
from .models import InvestmentPlan, UserInvestment, Investment, Deposit, Withdrawal, UserWallet


class InvestmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = "__all__"


class InvestmentSerializer(serializers.ModelSerializer):
    plan = InvestmentPlanSerializer(read_only=True)

    class Meta:
        model = Investment
        fields = [
            'id',
            'plan',
            'amount',
            'compound_interest',
            'profit',
            'total_return',
            'is_completed',
            'created_at',
            'ends_at'
        ]


class UserInvestmentSerializer(serializers.ModelSerializer):
    plan = InvestmentPlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=InvestmentPlan.objects.all(),
        source="plan",
        write_only=True
    )

    class Meta:
        model = UserInvestment
        fields = [
            "id", "plan", "plan_id", "amount", "start_date", "end_date",
            "status", "expected_profit", "total_payout"
        ]
        read_only_fields = ["start_date", "end_date", "expected_profit", "total_payout", "status"]

    def create(self, validated_data):
        user = self.context["request"].user
        plan = validated_data["plan"]
        amount = validated_data["amount"]

        # Check amount range
        if amount < plan.min_amount or amount > plan.max_amount:
            raise serializers.ValidationError("Amount is outside plan range.")

        investment = UserInvestment.objects.create(user=user, plan=plan, amount=amount)
        investment.calculate_expected_profit()
        investment.save()
        return investment


# ✅ Step 4: Serializer for ROI / Profit calculation
class InvestmentProfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ["id", "profit", "total_return", "is_completed"]


# ✅ Step 5: Serializers for Deposit and Withdrawal
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ["id", "user", "amount", "proof", "is_confirmed", "created_at"]
        read_only_fields = ["user", "is_confirmed", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ["id", "user", "amount", "wallet_address", "status", "created_at"]
        read_only_fields = ["user", "status", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)




class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ['id', 'balance', 'last_updated']
