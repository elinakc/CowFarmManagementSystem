from django.contrib import admin
from .models import Income, Expense
# from .views import FarmFinanceSummaryView
# Register your models here.
admin.site.register(Income)
admin.site.register(Expense)
# admin.site.register(FarmFinanceSummaryView)