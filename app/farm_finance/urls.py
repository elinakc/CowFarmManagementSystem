from django.urls import path
from .views import (
    IncomeListCreateAPIView,
    ExpenseListCreateAPIView,
    FarmFinanceSummaryView,
    ProfitLossView
)

urlpatterns = [
    path('incomes/', IncomeListCreateAPIView.as_view(), name='income-list-create'),
    path('expenses/', ExpenseListCreateAPIView.as_view(), name='expense-list-create'),
    path('finance-summary/', FarmFinanceSummaryView.as_view(), name='finance-summary'),
    path('profit-loss/', ProfitLossView.as_view(), name='profit-loss'),
]