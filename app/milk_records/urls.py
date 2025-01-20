from .import views
from django.urls import path, include
from .views import MilkRecordDetailView, MilkRecordListCreateView

urlpatterns = [
   
    path('milk-records/', MilkRecordListCreateView.as_view(), name='milk-record-list-create'),
    path('milk-records/<int:pk>/', MilkRecordDetailView.as_view(), name='milk-record-detail'),
]
