from django.db.models.signals import post_save
from django.dispatch import receiver
from investments.models import Deposit, Withdrawal, UserInvestment
from .models import TransactionHistory


@receiver(post_save, sender=Deposit)
def log_deposit_transaction(sender, instance, created, **kwargs):
    """Log a transaction whenever a deposit is approved."""
    if instance.status == 'approved':
        TransactionHistory.objects.get_or_create(
            user=instance.user,
            reference=f"DEP-{instance.id}",
            defaults={
                'transaction_type': 'deposit',
                'amount': instance.amount,
                'description': 'Deposit approved and credited to wallet',
                'status': 'successful',
                'balance_after': instance.user.wallet.balance
            }
        )


@receiver(post_save, sender=Withdrawal)
def log_withdrawal_transaction(sender, instance, created, **kwargs):
    """Log a transaction whenever a withdrawal is approved."""
    if instance.status == 'approved':
        TransactionHistory.objects.get_or_create(
            user=instance.user,
            reference=f"WDR-{instance.id}",
            defaults={
                'transaction_type': 'withdrawal',
                'amount': instance.amount,
                'description': 'Withdrawal approved and sent',
                'status': 'successful',
                'balance_after': instance.user.wallet.balance
            }
        )


@receiver(post_save, sender=UserInvestment)
def log_profit_transaction(sender, instance, created, **kwargs):
    """
    Log profit payout when an investment completes.
    Assumes you’ll trigger profit crediting logic when status changes to 'completed'.
    """
    if instance.status == 'completed':
        TransactionHistory.objects.get_or_create(
            user=instance.user,
            reference=f"INVPROFIT-{instance.id}",
            defaults={
                'transaction_type': 'profit',
                'amount': instance.expected_profit,
                'description': f'Profit from {instance.plan.name} investment',
                'status': 'successful',
                'balance_after': instance.user.wallet.balance
            }
        )
