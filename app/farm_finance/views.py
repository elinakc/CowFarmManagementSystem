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
    permission_classes = [AllowAny]
    serializer_class = IncomeSerializer  # Add this line
   
    def get_queryset(self):
        queryset = Income.objects.all().order_by('-date')
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')




        if year:
            queryset = queryset.filter(date__year=year)
        if month:
            queryset = queryset.filter(date__month=month)
       
        return queryset








class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ExpenseSerializer  # Add this line
   
    def get_queryset(self):
        queryset = Expense.objects.all().order_by('-date')
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')




        if year:
            queryset = queryset.filter(date__year=year)
        if month:
            queryset = queryset.filter(date__month=month)
       
        return queryset




     




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
        # Get the specified year and month from query parameters
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))




        current_date = timezone.now().date()
       
        # Calculate the date range for the specified year and month
        month_start = current_date.replace(year=year, month=month, day=1)
        if month == 12:
            month_end = month_start.replace(year=year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = month_start.replace(month=month + 1, day=1) - timedelta(days=1)




        # Calculate yearly range
        year_start = current_date.replace(year=year, month=1, day=1)
        year_end = current_date.replace(year=year + 1, month=1, day=1) - timedelta(days=1)




        # Get current month data for the specified month
        current_month_income = Income.objects.filter(
            date__range=[month_start, month_end]
        ).values('income_type').annotate(
            total=Sum('amount')
        )




        current_month_expenses = Expense.objects.filter(
            date__range=[month_start, month_end]
        ).values('expense_type').annotate(
            total=Sum('amount')
        )




        # Get yearly data
        yearly_income = Income.objects.filter(
            date__range=[year_start, year_end]
        ).values('income_type').annotate(total=Sum('amount'))




        yearly_expenses = Expense.objects.filter(
            date__range=[year_start, year_end]
        ).values('expense_type').annotate(total=Sum('amount'))




        # Calculate totals for the specified month
        current_total_income = sum(item['total'] for item in current_month_income)
        current_total_expenses = sum(item['total'] for item in current_month_expenses)




        # Calculate totals for the specified year
        total_income = sum(item['total'] for item in yearly_income)
        total_expenses = sum(item['total'] for item in yearly_expenses)




        # Calculate profit/loss for the specified month and year
        current_profit_loss = current_total_income - current_total_expenses
        net_profit_loss = total_income - total_expenses
       
        return Response({
            'month': month,
            'year': year,
            'current_month': {
                'total_income': current_total_income,
                'total_expenses': current_total_expenses,
                'net_profit_loss': current_profit_loss,
                'income_breakdown': list(current_month_income),
                'expense_breakdown': list(current_month_expenses)
            },
            'year': {
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net_profit_loss': net_profit_loss,
                'income_breakdown': list(yearly_income),
                'expense_breakdown': list(yearly_expenses)
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






