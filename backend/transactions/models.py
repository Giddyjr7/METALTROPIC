from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

User = settings.AUTH_USER_MODEL


class TransactionHistory(models.Model):
    """
    Logs all wallet activities such as deposits, withdrawals, profits, and manual adjustments.
    Keeps a full record of how each user's wallet balance changes over time.
    """

    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('profit', 'Profit'),
        ('manual_credit', 'Manual Credit'),
        ('manual_debit', 'Manual Debit'),
        ('transfer', 'Transfer'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='successful')
    balance_before = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reference = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Transaction History"
        verbose_name_plural = "Transaction Histories"

    def save(self, *args, **kwargs):
        """Automatically create a transaction reference if missing."""
        if not self.reference:
            self.reference = f"TXN-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ₦{self.amount}"


# --- SIGNALS SECTION ---
from django.db.models.signals import post_save
from django.dispatch import receiver
from investments.models import Deposit, Withdrawal
from wallets.models import Wallet



@receiver(post_save, sender=Deposit)
def log_deposit_transaction(sender, instance, created, **kwargs):
    """
    Automatically log a transaction when a deposit is approved.
    """
    if instance.status == 'approved':
        wallet, _ = UserWallet.objects.get_or_create(user=instance.user)
        before_balance = wallet.balance
        wallet.balance += instance.amount
        wallet.save()

        TransactionHistory.objects.create(
            user=instance.user,
            transaction_type='deposit',
            amount=instance.amount,
            balance_before=before_balance,
            balance_after=wallet.balance,
            status='successful',
            description=f"Deposit approved: {instance.transaction_id}",
        )


@receiver(post_save, sender=Withdrawal)
def log_withdrawal_transaction(sender, instance, created, **kwargs):
    """
    Automatically log a transaction when a withdrawal is approved.
    """
    if instance.status == 'approved':
        wallet, _ = UserWallet.objects.get_or_create(user=instance.user)
        before_balance = wallet.balance
        wallet.balance -= instance.amount
        wallet.save()

        TransactionHistory.objects.create(
            user=instance.user,
            transaction_type='withdrawal',
            amount=instance.amount,
            balance_before=before_balance,
            balance_after=wallet.balance,
            status='successful',
            description=f"Withdrawal approved: {instance.transaction_id}",
        )
