from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator
from decimal import Decimal

User = settings.AUTH_USER_MODEL


# -----------------------------
# INVESTMENT PLAN MODEL
# -----------------------------
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


# -----------------------------
# USER INVESTMENT MODEL
# -----------------------------
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
        daily_profit = (self.amount * self.plan.daily_roi) / 100
        total_profit = daily_profit * self.plan.duration_days
        self.expected_profit = total_profit
        self.total_payout = self.amount + total_profit
        return self.expected_profit


# -----------------------------
# INVESTMENT MODEL
# -----------------------------
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
        if not self.ends_at:
            self.ends_at = self.created_at + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def calculate_profit(self):
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


# -----------------------------
# DEPOSIT MODEL
# -----------------------------
class Deposit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(10)])
    proof = models.ImageField(upload_to='deposits/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def approve(self):
        if self.status != 'approved':
            self.status = 'approved'
            self.save(update_fields=["status", "updated_at"])
            # ✅ Update main wallet automatically (from wallets app)
            from wallets.models import Wallet
            wallet, _ = Wallet.objects.get_or_create(user=self.user)
            wallet.credit(self.amount)

    def reject(self):
        self.status = 'rejected'
        self.save(update_fields=["status", "updated_at"])

    def __str__(self):
        return f"Deposit {self.id} - {self.user.username} - ₦{self.amount} ({self.status})"


# -----------------------------
# WITHDRAWAL MODEL
# -----------------------------
class Withdrawal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="withdrawals")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(10)])
    wallet_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def approve(self):
        """Approve withdrawal only if user has enough balance."""
        from wallets.models import Wallet
        wallet, _ = Wallet.objects.get_or_create(user=self.user)
        if wallet.debit(self.amount):
            self.status = 'approved'
        else:
            self.status = 'rejected'
        self.save(update_fields=["status", "updated_at"])

    def reject(self):
        self.status = 'rejected'
        self.save(update_fields=["status", "updated_at"])

    def __str__(self):
        return f"Withdrawal {self.id} - {self.user.username} ({self.status})"
