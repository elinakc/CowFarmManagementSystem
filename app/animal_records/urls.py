from django.urls import path
from .views import AnimalListCreateView, AnimalDetailView

urlpatterns = [
    path('animal/', AnimalListCreateView.as_view(), name='animal-list-create'),
    path('animal/<int:pk>/', AnimalDetailView.as_view(), name='animal-detail')
]