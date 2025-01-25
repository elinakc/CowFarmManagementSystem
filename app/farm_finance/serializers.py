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
        
        
# class MonthlyFinanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MonthlyFinance
#         fields = '__all__'


# class QuarterlyFinanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QuarterlyFinance
#         fields = '__all__'


# class AnnualFinanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AnnualFinance
#         fields = '__all__'      
       