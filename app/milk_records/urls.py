from .import views
from django.urls import path, include
from .views import MilkRecordDetailView, MilkRecordListCreateView, CowListView, MonthlyMilkYieldView, ProfitLossCalculationView

urlpatterns = [
   
    path('milk-records/', MilkRecordListCreateView.as_view(), name='milk-record-list-create'),
    path('milk-records/<int:pk>/', MilkRecordDetailView.as_view(), name='milk-record-detail'),
    path('cows/', CowListView.as_view(), name='cow-list'),
    path('monthly-milk-yield/', MonthlyMilkYieldView.as_view(), name='monthly-milk-yield'),
    path('profit-loss/', ProfitLossCalculationView.as_view(), name='profit-loss-calculation'),
]

