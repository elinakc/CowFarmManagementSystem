from django.urls import path
from .views import (
    IncomeListCreateAPIView,
    ExpenseListCreateAPIView,
    FarmFinanceSummaryView,
    EnhancedFinancialSummaryView
    
    # ProfitLossView, 
    # MonthlyFinanceView, 
    # QuarterlyFinanceView, 
    # AnnualFinanceView
)

urlpatterns = [
    path('incomes/', IncomeListCreateAPIView.as_view(), name='income-list-create'),
    path('expenses/', ExpenseListCreateAPIView.as_view(), name='expense-list-create'),
    path('finance-summary/', FarmFinanceSummaryView.as_view(), name='finance-summary'),
   
    path('enhancedfinance-summary/', EnhancedFinancialSummaryView.as_view(), name='profit-loss'),
    
    # path('monthly-finance/', MonthlyFinanceView.as_view(), name='monthly-finance'),
    # path('quarterly-finance/', QuarterlyFinanceView.as_view(), name='quarterly-finance'),
    # path('annual-finance/', AnnualFinanceView.as_view(), name='annual-finance'),
]