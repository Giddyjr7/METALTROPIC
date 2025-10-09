from django.contrib import admin
from .models import InvestmentPlan, UserInvestment

# Register your models here.
admin.site.register(InvestmentPlan)
admin.site.register(UserInvestment)
