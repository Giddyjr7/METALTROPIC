from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()
User = settings.AUTH_USER_MODEL

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



class Investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    compound_interest = models.BooleanField(default=False)
    profit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_return = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-set end date
        if not self.ends_at:
            self.ends_at = self.created_at + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def calculate_profit(self):
        """Calculate profit and total returns"""
        daily_rate = self.plan.daily_roi / 100
        days = self.plan.duration_days

        if self.compound_interest:
            final_amount = float(self.amount)
            for _ in range(days):
                final_amount += final_amount * daily_rate
            profit = final_amount - float(self.amount)
        else:
            profit = float(self.amount) * daily_rate * days

        self.profit = profit
        self.total_return = float(self.amount) + profit
        self.is_completed = timezone.now() >= self.ends_at
        self.save()
        return profit
    

class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(10)])
    proof = models.ImageField(upload_to='deposits/')
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deposit {self.id} by {self.user.username}"


class Withdrawal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Withdrawal {self.id} - {self.user.username} ({self.status})"
    


class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

    def credit(self, amount):
        """Add funds to the wallet."""
        self.balance += Decimal(amount)
        self.save()

    def debit(self, amount):
        """Subtract funds from the wallet (only if sufficient balance)."""
        if self.balance >= Decimal(amount):
            self.balance -= Decimal(amount)
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"
