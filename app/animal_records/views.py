from django.shortcuts import render
from rest_framework.response import Response
from .serializers import AnimalRecordsSerializer
from .models import AnimalRecords
from rest_framework.views import APIView
from rest_framework import status
from app.Users_app.permissions import role_required, IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


import logging

logger = logging.getLogger(__name__)


class AnimalListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    
    @role_required(['admin'])
    def get(self, request):
        """List all animals"""
        animal = AnimalRecords.objects.all()
        serializers = AnimalRecordsSerializer(animal, many=True)
        return Response(serializers.data)
    
    @role_required(['admin'])
    def post(self, request):
        """Create a new animal record"""
        logger.info(f"Received data: {request.data}")
        
        serializer = AnimalRecordsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                logger.info("Animal record saved successfully")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error saving animal record: {str(e)}")
                return Response(
                    {"detail": "Error saving animal record", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        logger.error(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AnimalDetailView(APIView):
    permission_classes =[IsAdmin]
    @role_required(['admin'])
 
    
    def get_object(self, pk):
        try:
            return AnimalRecords.objects.get(pk=pk)
        except AnimalRecords.DoesNotExist:
            return None

    @role_required(['admin'])
    def get(self, request, pk):
        animal = self.get_object(pk)
        if animal:
            serializer = AnimalRecordsSerializer(animal)
            return Response(serializer.data)
        return Response({"error": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)

    @role_required(['admin'])
    def put(self, request, pk):
        animal = self.get_object(pk)
        if animal:
            serializer = AnimalRecordsSerializer(
                animal, data=request.data, partial=False
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @role_required(['admin'])
    def patch(self, request, pk):
        animal = self.get_object(pk)
        if animal:
            serializer = AnimalRecordsSerializer(
                animal, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)

    @role_required(['admin'])
    def delete(self, request, pk):
        animal = self.get_object(pk)
        if animal:
            animal.delete()
            return Response(
                {"message": "Animal record deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"message": "Animal Not found"}, status=status.HTTP_404_NOT_FOUND
        )