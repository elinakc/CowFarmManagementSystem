from django.shortcuts import render
from .models import HealthRecord
from .serializers import HealthRecordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class HealthRecordListCreateView(APIView):
  
  def get(self, request):
        health_records = HealthRecord.objects.all()
        serializers = HealthRecordSerializer(health_records, many=True)
        return Response(serializers.data)
      
  @swagger_auto_schema(
        request_body=HealthRecordSerializer,
        responses={
            201: HealthRecordSerializer,
            400: openapi.Response("Bad Request"),
        },
    )
  def post(self, request):
        serializer = HealthRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HealthRecordDetailView(APIView):
  @swagger_auto_schema(
        responses={
            200: HealthRecordSerializer,
            404: openapi.Response("Animal not found"),
        },
    )
  def get_object(self, pk):
        try:
            return HealthRecord.objects.get(pk=pk)
        except HealthRecord.DoesNotExist:
            return None

  def get(self, request, pk):
        health_record = self.get_object(pk)
        if health_record:
            serializer = HealthRecordSerializer(health_record)
            return Response(serializer.data)
        return Response(
            {"error": "Health Record not found"}, status=status.HTTP_400_BAD_REQUEST
        )

  def put(self, request, pk):
        health_record = self.get_object(pk)
        if health_record:
            serializer = HealthRecordSerializer(
                health_record, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "Health record not found"}, status=status.HTTP_404_NOT_FOUND
        )

  def delete(self, request, pk):
        health_record = self.get_object(pk)
        if health_record:
            health_record.delete()
            return Response(
                {"message": "Health record deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"error": "Health record not found"}, status=status.HTTP_404_NOT_FOUND
        )
