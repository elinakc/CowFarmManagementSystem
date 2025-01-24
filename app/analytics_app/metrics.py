from django.db.models import Count, Avg, Sum, F,Q
from django.db.models.functions import ExtractYear, Now
from datetime import  date
from django.db.models.functions import ExtractYear, Now, TruncMonth
from app.animal_records.models import AnimalRecords
from app.health_records.models import HealthRecord
from app.milk_records.models import MilkRecord
from app.farm_finance.models import Income, Expense
from django.utils import timezone

class AnimalAnalyticsService:
    @staticmethod
    def get_breed_analytics():
        """Analyze breed distribution and performance"""
        breed_stats = AnimalRecords.objects.values('breed').annotate(
            count=Count('id'),
            avg_milk_yield=Avg('daily_milk_yield'),
            total_milk_yield=Sum('monthly_milk_yield')
        ).order_by('-count')

        total_animals = AnimalRecords.objects.count()
        
        return {
            'total_animals': total_animals,
            'breed_distribution': list(breed_stats),
            'top_performing_breed': breed_stats.order_by('-avg_milk_yield').first()
         }

    @staticmethod
    def get_milk_production_analytics():
        """Analyze milk production statistics"""
        return {
            'overall_stats': AnimalRecords.objects.aggregate(
                avg_daily_yield=Avg('daily_milk_yield'),
                avg_monthly_yield=Avg('monthly_milk_yield'),
                total_monthly_production=Sum('monthly_milk_yield')
            ),
            'by_lactation_cycle': AnimalRecords.objects.values('lactation_cycle').annotate(
                count=Count('id'),
                avg_daily_yield=Avg('daily_milk_yield'),
                total_yield=Sum('monthly_milk_yield')
            ).order_by('lactation_cycle'),
        }

    @staticmethod
    def get_pregnancy_analytics():
        """Analyze pregnancy and breeding statistics"""
        total_animals = AnimalRecords.objects.count()
        pregnant_count = AnimalRecords.objects.filter(pregnancy_status=True).count()
        
        return {
            'total_animals': total_animals,
            'pregnant_count': pregnant_count,
            'pregnancy_rate': (pregnant_count / total_animals * 100) if total_animals > 0 else 0,
            'due_dates': list(AnimalRecords.objects.filter(
                pregnancy_status=True,
                due_date__isnull=False
            ).values('name', 'due_date').order_by('due_date')),
            'lactation_status': AnimalRecords.objects.values('lactation_cycle').annotate(
                count=Count('id')
            ).order_by('lactation_cycle')
        }

    @staticmethod
    def get_age_analytics():
        """Analyze age distribution"""
        today = date.today()
        return AnimalRecords.objects.annotate(
            age_years=ExtractYear(Now()) - ExtractYear('dob')
        ).aggregate(
            average_age=Avg('age_years'),
            total_animals=Count('id'),
            young_count=Count('id', filter=Q(age_years__lt=2)),
            adult_count=Count('id', filter=Q(age_years__range=(2, 5))),
            senior_count=Count('id', filter=Q(age_years__gt=5))
        )

    @staticmethod
    def get_comprehensive_report():
        """Generate comprehensive analytics report"""
        return {
            'breed_analytics': AnimalAnalyticsService.get_breed_analytics(),
            'milk_production': AnimalAnalyticsService.get_milk_production_analytics(),
            'pregnancy_stats': AnimalAnalyticsService.get_pregnancy_analytics(),
            'age_distribution': AnimalAnalyticsService.get_age_analytics()
        }
class MilkProductionAnalytics:
    @staticmethod
    def get_milk_production_insights(start_date=None, end_date=None):
        """Analyze milk production patterns"""
        queryset = MilkRecord.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(milking_date__range=[start_date, end_date])

        return {
            'daily_averages': queryset.annotate(
                total_daily=F('morning_milk_quantity') + 
                           F('afternoon_milk_quantity') + 
                           F('evening_milk_quantity')
            ).aggregate(
                avg_daily_production=Avg('total_daily'),
                avg_morning=Avg('morning_milk_quantity'),
                avg_afternoon=Avg('afternoon_milk_quantity'),
                avg_evening=Avg('evening_milk_quantity')
            ),
            
            'monthly_trends': queryset.annotate(
                month=TruncMonth('milking_date'),
                daily_total=F('morning_milk_quantity') + 
                           F('afternoon_milk_quantity') + 
                           F('evening_milk_quantity')
            ).values('month').annotate(
                total_production=Sum('daily_total'),
                avg_daily_production=Avg('daily_total')
            ).order_by('month'),
            
            'top_producing_cows': queryset.values(
                'cow__name', 'cow__breed'
            ).annotate(
                total_production=Sum(
                    F('morning_milk_quantity') + 
                    F('afternoon_milk_quantity') + 
                    F('evening_milk_quantity')
                )
            ).order_by('-total_production')[:5]
        }

class HealthAnalytics:
    @staticmethod
    def get_health_insights(start_date=None, end_date=None):
        """Analyze health patterns and costs"""
        queryset = HealthRecord.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=[start_date, end_date])

        return {
            'health_condition_summary': queryset.values(
                'health_condtion'
            ).annotate(
                count=Count('id'),
                avg_treatment_cost=Avg('treatment_cost'),
                total_cost=Sum('treatment_cost')
            ).order_by('-count'),
            
            'recovery_statistics': queryset.values(
                'recovery_status'
            ).annotate(
                count=Count('id')
            ).order_by('-count'),
            
            'treatment_costs': queryset.values(
                month=TruncMonth('created_at')
            ).annotate(
                total_cost=Sum('treatment_cost'),
                avg_cost=Avg('treatment_cost')
            ).order_by('month'),
            
            'common_illnesses': queryset.exclude(
                diagnosed_illness__isnull=True
            ).values('diagnosed_illness').annotate(
                count=Count('id')
            ).order_by('-count')[:5]
        }
    
class FinancialAnalytics:
    @staticmethod
    def get_financial_insights(start_date=None, end_date=None):
        """Analyze financial performance"""
        income_queryset = Income.objects.all()
        expense_queryset = Expense.objects.all()
        
        if start_date and end_date:
            income_queryset = income_queryset.filter(date__range=[start_date, end_date])
            expense_queryset = expense_queryset.filter(date__range=[start_date, end_date])

        monthly_income = income_queryset.annotate(
            month=TruncMonth('date')
        ).values('month', 'income_type').annotate(
            total=Sum('amount')
        ).order_by('month', 'income_type')

        monthly_expenses = expense_queryset.annotate(
            month=TruncMonth('date')
        ).values('month', 'expense_type').annotate(
            total=Sum('amount')
        ).order_by('month', 'expense_type')

        return {
            'income_summary': {
                'total_income': income_queryset.aggregate(total=Sum('amount'))['total'],
                'by_type': income_queryset.values('income_type').annotate(
                    total=Sum('amount')
                ).order_by('-total'),
                'monthly_trends': monthly_income
            },
            'expense_summary': {
                'total_expenses': expense_queryset.aggregate(total=Sum('amount'))['total'],
                'by_type': expense_queryset.values('expense_type').annotate(
                    total=Sum('amount')
                ).order_by('-total'),
                'monthly_trends': monthly_expenses
            },
            'profitability': {
                'net_income': income_queryset.aggregate(
                    total=Sum('amount')
                )['total'] - expense_queryset.aggregate(total=Sum('amount'))['total'],
                'monthly_profit': income_queryset.annotate(
                    month=TruncMonth('date')
                ).values('month').annotate(
                    income=Sum('amount')
                ).order_by('month')
            }
        }
class ComprehensiveAnalytics:
    @staticmethod
    def get_farm_performance_metrics(start_date=None, end_date=None):
        """Get comprehensive farm performance metrics"""
        return {
            'milk_production': MilkProductionAnalytics.get_milk_production_insights(
                start_date, end_date
            ),
            'health_metrics': HealthAnalytics.get_health_insights(
                start_date, end_date
            ),
            'financial_metrics': FinancialAnalytics.get_financial_insights(
                start_date, end_date
            ),
            'timestamp': timezone.now()
        }
