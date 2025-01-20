from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from app.milk_records.models import MilkRecord
from app.health_records.models import HealthRecord

from.models import Income
from .models import Expense

from .serializers import IncomeSerializer, ExpenseSerializer

class IncomeListCreateAPIView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        animal_id = request.query_params.get('animal_id')
        income_type = request.query_params.get('income_type')
        
        incomes = Income.objects.all()
        
        if start_date and end_date:
            incomes = incomes.filter(date__range=[start_date, end_date])
        if animal_id:
            incomes = incomes.filter(animal_id=animal_id)
        if income_type:
            incomes = incomes.filter(income_type=income_type)
            
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            # Auto-link to milk record if it's a milk sale
            if serializer.validated_data['income_type'] == 'MILK' and 'milk_record' not in serializer.validated_data:
                milk_record = MilkRecord.objects.filter(
                    date=serializer.validated_data['date'],
                    animal=serializer.validated_data.get('animal')
                ).first()
                if milk_record:
                    serializer.validated_data['milk_record'] = milk_record
            
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseListCreateAPIView(APIView):
    def get(self, request):
        # Add filtering capabilities
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        animal_id = request.query_params.get('animal_id')
        expense_type = request.query_params.get('expense_type')
        health_record_id = request.query_params.get('health_record_id')
        
        expenses = Expense.objects.all()
        
        # Apply filters if provided
        if start_date and end_date:
            expenses = expenses.filter(date__range=[start_date, end_date])
        if animal_id:
            expenses = expenses.filter(animal_id=animal_id)
        if expense_type:
            expenses = expenses.filter(expense_type=expense_type)
        if health_record_id:
            expenses = expenses.filter(health_record_id=health_record_id)
            
        # Order by date descending (newest first)
        expenses = expenses.order_by('-date')
        
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            # Auto-link to health record if it's a veterinary expense
            if (serializer.validated_data['expense_type'] == 'VET' and 
                'health_record' not in serializer.validated_data and 
                'animal' in serializer.validated_data):
                
                health_record = HealthRecord.objects.filter(
                    date=serializer.validated_data['date'],
                    animal=serializer.validated_data['animal']
                ).first()
                
                if health_record:
                    serializer.validated_data['health_record'] = health_record
            
            # Save with the current user
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FarmFinanceSummaryView(APIView):
    def get(self, request):
        end_date = request.query_params.get('end_date', now().date())
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
        start_date = request.query_params.get('start_date', (end_date - relativedelta(months=1)))
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        # Get detailed breakdown
        milk_income = Income.objects.filter(
            date__range=[start_date, end_date],
            income_type='MILK'
        ).aggregate(total=Sum('amount'))['total'] or 0

        cattle_income = Income.objects.filter(
            date__range=[start_date, end_date],
            income_type='CATTLE'
        ).aggregate(total=Sum('amount'))['total'] or 0

        feed_expenses = Expense.objects.filter(
            date__range=[start_date, end_date],
            expense_type='FEED'
        ).aggregate(total=Sum('amount'))['total'] or 0

        vet_expenses = Expense.objects.filter(
            date__range=[start_date, end_date],
            expense_type='VET'
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_income = milk_income + cattle_income
        total_expenses = feed_expenses + vet_expenses
        net_profit = total_income - total_expenses

        # Get per-animal statistics
        animal_stats = Income.objects.filter(
            date__range=[start_date, end_date],
            animal__isnull=False
        ).values('animal').annotate(
            total_income=Sum('amount'),
            transaction_count=Count('id')
        ).order_by('-total_income')

        summary_data = {
            "total_income": total_income,
            "milk_income": milk_income,
            "cattle_income": cattle_income,
            "total_expenses": total_expenses,
            "feed_expenses": feed_expenses,
            "vet_expenses": vet_expenses,
            "net_profit": net_profit,
            "period_start": start_date,
            "period_end": end_date,
            "top_performing_animals": list(animal_stats[:5])
        }

        return Response(summary_data)
    
class ProfitLossView(APIView):
    def get(self, request):
        # Get date range from query parameters
        end_date = request.query_params.get('end_date', datetime.now().date())
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
        start_date = request.query_params.get('start_date', (end_date - relativedelta(months=1)))
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        # Get income breakdown
        income_breakdown = Income.objects.filter(
            date__range=[start_date, end_date]
        ).values('income_type').annotate(
            total=Sum('amount'),
            count=Count('id')
        )

        # Get expense breakdown
        expense_breakdown = Expense.objects.filter(
            date__range=[start_date, end_date]
        ).values('expense_type').annotate(
            total=Sum('amount'),
            count=Count('id')
        )

        # Calculate totals
        total_income = sum(item['total'] for item in income_breakdown)
        total_expenses = sum(item['total'] for item in expense_breakdown)
        net_profit = total_income - total_expenses
        profit_margin = (net_profit / total_income * 100) if total_income > 0 else 0

        # Get monthly trend
        monthly_profits = []
        current_date = start_date
        while current_date <= end_date:
            month_end = min(
                current_date + relativedelta(months=1, days=-1),
                end_date
            )
            
            month_income = Income.objects.filter(
                date__range=[current_date, month_end]
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            month_expenses = Expense.objects.filter(
                date__range=[current_date, month_end]
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            monthly_profits.append({
                'month': current_date.strftime('%Y-%m'),
                'income': month_income,
                'expenses': month_expenses,
                'profit': month_income - month_expenses
            })
            
            current_date += relativedelta(months=1)

        return Response({
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'summary': {
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net_profit': net_profit,
                'profit_margin_percentage': round(profit_margin, 2)
            },
            'income_breakdown': income_breakdown,
            'expense_breakdown': expense_breakdown,
            'monthly_trend': monthly_profits
        })