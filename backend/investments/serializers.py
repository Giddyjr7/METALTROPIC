from rest_framework import serializers
from .models import InvestmentPlan, UserInvestment


class InvestmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = "__all__"


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
