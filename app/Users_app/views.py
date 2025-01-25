from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegistrationSerializer, loginSerializer
from .permissions import role_required, IsVeterinarian, IsAdmin, IsManager
from app.animal_records.models import AnimalRecords
from app.milk_records.models import MilkRecord
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to register

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()  # Save user
            # Create a token for the new user
            token =get_tokens_for_user(user)
            
            return Response({
                'message': "User Registration Successful",
                'user_email': user.email,
                'roles': user.roles,
                'token': token  # Return token upon registration
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to attempt login

    @role_required(['admin', 'vet', 'manager'])  # Custom role-based access
    def post(self, request):
        serializer = loginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']  # Retrieve validated user
            # Create or retrieve a token for the user
            token =get_tokens_for_user(user)

            return Response({
                'message': 'Login successful',
                'token': token,  # Return token to the user
                'email': user.email,
                'roles': user.roles
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def post(self, request):
        # Delete the user's token to log them out
        if request.auth:
            request.auth.delete()  # Remove the token
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "No active session found."}, status=status.HTTP_400_BAD_REQUEST)


# Admin Dashboard View
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        total_animals = AnimalRecords.objects.count()
        total_milk_records = MilkRecord.objects.count()
        

        data = {
            "dashboard": "Admin Dashboard",
            "total_users": 100,
            "active_farms": 10,
            "total_animals": total_animals,
            "total_milk_records": total_milk_records,
            
        }
        return Response(data)




# Veterinarian Dashboard View
class VeterinarianDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsVeterinarian]

    def get(self, request):
        # Fetch veterinarian-specific data (e.g., assigned tasks, animals to check)
        data = {
            "dashboard": "Veterinarian Dashboard",
            "tasks": ["Check cow A", "Vaccinate cow B"],
            "total_animals": 50,
        }
        return Response(data)

# Manager Dashboard View
class ManagerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        # Fetch manager-specific data (e.g., resource allocation, farm reports)
        data = {
            "dashboard": "Manager Dashboard",
            "monthly_reports": ["Report 1", "Report 2"],
            "active_projects": 5,
        }
        return Response(data)


