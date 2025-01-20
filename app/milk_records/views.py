from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import MilkRecord
from .serializers import MilkRecordSerializer
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import  permissions, status


class MilkRecordListCreateView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        operation_summary="List all milk records",
        responses={200: MilkRecordSerializer(many=True)}
    )
    
    def get(self, request):
        "List all milk records"
        milk_records = MilkRecord.objects.all()
        serializer = MilkRecordSerializer(milk_records, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Create a new milk record",
        request_body=MilkRecordSerializer,
        responses={201: MilkRecordSerializer}
    )

    def post(self, request):
        "Create a new milk record"
        serializer = MilkRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MilkRecordDetailView(APIView):
   
    @swagger_auto_schema(
        operation_summary="Retrieve a specific milk record",
        responses={200: MilkRecordSerializer, 404: "Milk record not found"}
    )
   
    def get_object(self, pk):
        try:
            return MilkRecord.objects.get(pk=pk)
        except MilkRecord.DoesNotExist:
            return None

    def get(self, request, pk):
        """Retrieve a specific milk record"""
        milk_record = self.get_object(pk)
        if milk_record:
            serializer = MilkRecordSerializer(milk_record)
            return Response(serializer.data)
        return Response(
            {"error": "Milk record not found"}, status=status.HTTP_404_NOT_FOUND
        )
    @swagger_auto_schema(
        operation_summary="Update a specific milk record",
        request_body=MilkRecordSerializer,
        responses={200: MilkRecordSerializer, 404: "Milk record not found"}
    )

    def put(self, request, pk):
        """Update a specific milk record"""
        milk_record = self.get_object(pk)
        if milk_record:
            serializer = MilkRecordSerializer(
                milk_record, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "Milk record not found"}, status=status.HTTP_404_NOT_FOUND
        )
    @swagger_auto_schema(
        operation_summary="Delete a specific milk record",
        responses={204: "Milk record deleted successfully", 404: "Milk record not found"}
    )
    def delete(self, request, pk):
        """Delete a specific milk record"""
        milk_record = self.get_object(pk)
        if milk_record:
            milk_record.delete()
            return Response(
                {"message": "Milk record deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"error": "Milk record not found"}, status=status.HTTP_404_NOT_FOUND
        )
