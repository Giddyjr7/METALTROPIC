from django.db import models
from django.conf import settings

class InvestmentPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    daily_roi = models.DecimalField(max_digits=5, decimal_places=2, help_text="Daily ROI in percentage")
    duration_days = models.PositiveIntegerField()
    total_return = models.DecimalField(max_digits=5, decimal_places=2, help_text="Total ROI + Capital")
    compound_interest = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserInvestment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="investments")
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name="user_investments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    expected_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_payout = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    def calculate_expected_profit(self):
        """Calculates expected profit based on ROI and duration."""
        daily_profit = (self.amount * self.plan.daily_roi) / 100
        total_profit = daily_profit * self.plan.duration_days
        self.expected_profit = total_profit
        self.total_payout = self.amount + total_profit
        return self.expected_profit
