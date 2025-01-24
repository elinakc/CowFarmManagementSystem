from django.urls import path
from .views import HealthRecordDetailView, HealthRecordListCreateView, CowListView

urlpatterns = [
   
  path("health-records/", HealthRecordListCreateView.as_view(), name="health-record-list"),
  path("health-records/<int:pk>/", HealthRecordDetailView.as_view(), name="health-record-detail"),
   path('cows/', CowListView.as_view(), name='cow-list'),
]
