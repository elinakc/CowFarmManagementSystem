from .import views
from django.urls import path, include
from rest_framework.routers  import DefaultRouter
from .views import UserRegistrationView, loginView, LogoutView

router =DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', loginView.as_view(), name='login'),
    path('logout/',  LogoutView.as_view(), name='login'),
   


]