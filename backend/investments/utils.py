from django.utils import timezone
from decimal import Decimal

def update_investment_profits(user):
    from .models import Investment

    investments = Investment.objects.filter(user=user, is_completed=False)
    updated = 0

    for inv in investments:
        if timezone.now() >= inv.ends_at:
            inv.calculate_profit()
            inv.is_completed = True
            inv.save()
        else:
            inv.calculate_profit()
        updated += 1

    return updated
