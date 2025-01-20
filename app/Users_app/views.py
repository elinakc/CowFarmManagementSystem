
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from .serializers import  UserRegistrationSerializer, loginSerializer
from rest_framework import  permissions, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(request_body= UserRegistrationSerializer)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': "User Registration Successful",
                'user_email': user.email,
                'roles': user.roles,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class loginView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(request_body= loginSerializer)
    
    def post(self, request):
        serializers =loginSerializer(data = request.data)
        
        if serializers.is_valid():
            user = serializers.validated_data['user']
            
            # token, created =Token.objects.get_or_create(user=user)
            
            return Response({
                'message':'login successfully',
                # 'token':Token.key,
                'email':user.pk,
                'roles':user.roles
             
        })
        return Response(serializers.errors, status =status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema( responses={200: openapi.Response('Logout Successful')} )

    def post(self, request):
        # Remove the user token to log out
        if request.auth:
            request.auth.delete()
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "No active session found."}, status=status.HTTP_400_BAD_REQUEST)






