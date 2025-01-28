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

class ProfitLossView(APIView):
    permission_classes =[AllowAny]
    # permission_classes = [IsAdmin | IsManager]
    # @role_required(['admin','manager']) 
    
    def get(self, request):
        # Get date range from query parameters or use default (last 30 days)
        end_date = request.query_params.get('end_date', timezone.now().date())
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
       
        start_date = request.query_params.get('start_date', end_date - timedelta(days=30))
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()


        # Get income breakdown by type
        income_by_type = Income.objects.filter(
            date__range=[start_date, end_date]
        ).values('income_type').annotate(
            total=Sum('amount')
        )


        # Get expense breakdown by type
        expense_by_type = Expense.objects.filter(
            date__range=[start_date, end_date]
        ).values('expense_type').annotate(
            total=Sum('amount')
        )


        # Calculate totals
        total_income = sum(item['total'] for item in income_by_type)
        total_expenses = sum(item['total'] for item in expense_by_type)
        net_profit = total_income - total_expenses


        return Response({
            'startDate': start_date,
            'endDate': end_date,
            'incomeBreakdown': income_by_type,
            'expenseBreakdown': expense_by_type,
            'totalIncome': total_income,
            'totalExpenses': total_expenses,
            'netProfit': net_profit
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




