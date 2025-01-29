from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Income, Expense
from .serializers import IncomeSerializer, ExpenseSerializer
from app.Users_app.permissions import IsAdmin, IsManager, role_required
from rest_framework.permissions import AllowAny

class IncomeListCreateAPIView(generics.ListCreateAPIView):
    # permission_classes = [IsAdmin | IsManager]
    permission_classes =[AllowAny]
    queryset = Income.objects.all().order_by('-date')
    serializer_class = IncomeSerializer

   
class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    permission_classes =[AllowAny]
    # permission_classes = [IsAdmin | IsManager]
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer

  
        

class FarmFinanceSummaryView(APIView):
    permission_classes =[AllowAny]
    # permission_classes = [IsAdmin | IsManager]
    # @role_required(['admin','manager']) 
    
    def get(self, request):
        # Get total income
        total_income = Income.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Get total expenses
        total_expenses = Expense.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Calculate net profit and cash balance
        net_profit = total_income - total_expenses
        cash_balance = net_profit  # You might want to adjust this based on your business logic

        return Response({
            'totalIncome': total_income,
            'totalExpenses': total_expenses,
            'netProfit': net_profit,
            'cashBalance': cash_balance
            
        })
        
class EnhancedFinancialSummaryView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Get current date and date ranges
        current_date = timezone.now().date()
        
        # Current month range
        current_month_start = current_date.replace(day=1)
        if current_date.month == 12:
            current_month_end = current_date.replace(year=current_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            current_month_end = current_date.replace(month=current_date.month + 1, day=1) - timedelta(days=1)
            
        # Previous month range
        if current_date.month == 1:
            prev_month_start = current_date.replace(year=current_date.year - 1, month=12, day=1)
            prev_month_end = current_month_start - timedelta(days=1)
        else:
            prev_month_start = current_date.replace(month=current_date.month - 1, day=1)
            prev_month_end = current_month_start - timedelta(days=1)
            
        # Year to date range
        year_start = current_date.replace(month=1, day=1)
        
        # Get current month data
        current_month_income = Income.objects.filter(
            date__range=[current_month_start, current_month_end]
        ).values('income_type').annotate(
            total=Sum('amount')
        )
        
        current_month_expenses = Expense.objects.filter(
            date__range=[current_month_start, current_month_end]
        ).values('expense_type').annotate(
            total=Sum('amount')
        )
        
        # Get previous month data
        prev_month_income = Income.objects.filter(
            date__range=[prev_month_start, prev_month_end]
        ).values('income_type').annotate(
            total=Sum('amount')
        )
        
        prev_month_expenses = Expense.objects.filter(
            date__range=[prev_month_start, prev_month_end]
        ).values('expense_type').annotate(
            total=Sum('amount')
        )
        
        # Get year-to-date data
        ytd_income = Income.objects.filter(
            date__range=[year_start, current_date]
        ).values('income_type').annotate(
            total=Sum('amount')
        )
        
        ytd_expenses = Expense.objects.filter(
            date__range=[year_start, current_date]
        ).values('expense_type').annotate(
            total=Sum('amount')
        )
        
        # Calculate totals
        current_total_income = sum(item['total'] for item in current_month_income)
        current_total_expenses = sum(item['total'] for item in current_month_expenses)
        prev_total_income = sum(item['total'] for item in prev_month_income)
        prev_total_expenses = sum(item['total'] for item in prev_month_expenses)
        ytd_total_income = sum(item['total'] for item in ytd_income)
        ytd_total_expenses = sum(item['total'] for item in ytd_expenses)
        
        # Calculate profit/loss
        current_profit_loss = current_total_income - current_total_expenses
        prev_profit_loss = prev_total_income - prev_total_expenses
        ytd_profit_loss = ytd_total_income - ytd_total_expenses
        
        # Calculate daily averages
        days_in_month = (current_month_end - current_month_start).days + 1
        daily_avg_income = current_total_income / days_in_month if days_in_month > 0 else 0
        daily_avg_expenses = current_total_expenses / days_in_month if days_in_month > 0 else 0
        
        # Calculate percentage breakdowns
        def calculate_percentages(items, total):
            return [
                {**item, 'percentage': round((item['total'] / total * 100), 2)}
                for item in items
            ] if total > 0 else items

        income_with_percentages = calculate_percentages(list(current_month_income), current_total_income)
        expenses_with_percentages = calculate_percentages(list(current_month_expenses), current_total_expenses)
        
        # Calculate month-over-month changes
        income_change = round(((current_total_income - prev_total_income) / prev_total_income * 100), 2) if prev_total_income > 0 else 0
        expense_change = round(((current_total_expenses - prev_total_expenses) / prev_total_expenses * 100), 2) if prev_total_expenses > 0 else 0
        profit_change = round(((current_profit_loss - prev_profit_loss) / abs(prev_profit_loss) * 100), 2) if prev_profit_loss != 0 else 0
        
        return Response({
            'current_month': {
                'month': current_date.strftime('%B %Y'),
                'income': {
                    'breakdown': income_with_percentages,
                    'total': current_total_income,
                    'daily_average': round(daily_avg_income, 2)
                },
                'expenses': {
                    'breakdown': expenses_with_percentages,
                    'total': current_total_expenses,
                    'daily_average': round(daily_avg_expenses, 2)
                },
                'net_profit_loss': current_profit_loss,
                'status': 'Profit' if current_profit_loss >= 0 else 'Loss'
            },
            'comparison_with_previous_month': {
                'income_change_percentage': income_change,
                'expense_change_percentage': expense_change,
                'profit_loss_change_percentage': profit_change,
                'previous_month_totals': {
                    'income': prev_total_income,
                    'expenses': prev_total_expenses,
                    'profit_loss': prev_profit_loss
                }
            },
            'year_to_date': {
                'total_income': ytd_total_income,
                'total_expenses': ytd_total_expenses,
                'net_profit_loss': ytd_profit_loss,
                'income_breakdown': list(ytd_income),
                'expense_breakdown': list(ytd_expenses)
            },
            'summary_metrics': {
                'profit_margin': round((current_profit_loss / current_total_income * 100), 2) if current_total_income > 0 else 0,
                'expense_ratio': round((current_total_expenses / current_total_income * 100), 2) if current_total_income > 0 else 0
            }
        })



# @role_required(['admin','manager']) 
class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdmin | IsManager]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

# @role_required(['admin','manager']) 
class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdmin | IsManager]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer




