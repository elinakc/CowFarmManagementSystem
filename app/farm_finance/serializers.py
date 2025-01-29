from rest_framework import serializers
from .models import Income, Expense

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [ 'date', 'income_type', 'amount']
          

class ExpenseSerializer(serializers.ModelSerializer):
   class Meta:
        model = Expense
        fields = [ 'date', 'expense_type',  'amount']
        
        
class BreakdownSerializer(serializers.Serializer):
    income_type = serializers.CharField(required=False)  # For income breakdown
    expense_type = serializers.CharField(required=False)  # For expense breakdown
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)

class IncomeExpenseDetailSerializer(serializers.Serializer):
    breakdown = BreakdownSerializer(many=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    daily_average = serializers.DecimalField(max_digits=12, decimal_places=2)

class CurrentMonthSerializer(serializers.Serializer):
    month = serializers.CharField()
    income = IncomeExpenseDetailSerializer()
    expenses = IncomeExpenseDetailSerializer()
    net_profit_loss = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.CharField()

class PreviousMonthTotalsSerializer(serializers.Serializer):
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit_loss = serializers.DecimalField(max_digits=12, decimal_places=2)

class ComparisonSerializer(serializers.Serializer):
    income_change_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    expense_change_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    profit_loss_change_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    previous_month_totals = PreviousMonthTotalsSerializer()

class YearToDateSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_profit_loss = serializers.DecimalField(max_digits=12, decimal_places=2)
    income_breakdown = BreakdownSerializer(many=True)
    expense_breakdown = BreakdownSerializer(many=True)

class SummaryMetricsSerializer(serializers.Serializer):
    profit_margin = serializers.DecimalField(max_digits=5, decimal_places=2)
    expense_ratio = serializers.DecimalField(max_digits=5, decimal_places=2)

class EnhancedMonthlyFinancialSummarySerializer(serializers.Serializer):
    current_month = CurrentMonthSerializer()
    comparison_with_previous_month = ComparisonSerializer()
    year_to_date = YearToDateSerializer()
    summary_metrics = SummaryMetricsSerializer()