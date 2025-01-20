from django.shortcuts import render
from rest_framework.response import Response
from .serializers import AnimalRecordsSerializer
from .models import AnimalRecords
from rest_framework.views import APIView
from rest_framework import status
from app.schemas import CustomSchema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CreateAnimalView(APIView):
    schema = CustomSchema()
    @swagger_auto_schema(
        request_body=AnimalRecordsSerializer,
        responses={
            201: AnimalRecordsSerializer,
            400: openapi.Response("Bad Request"),
        },
    )
    def post(self, request):
        serializer = AnimalRecordsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnimalDetailView(APIView):
    schema = CustomSchema()
    @swagger_auto_schema(
        responses={
            200: AnimalRecordsSerializer,
            404: openapi.Response("Animal not found"),
        },
    )
    def get_object(self, pk):
        try:
            return AnimalRecords.objects.get(pk=pk)
        except AnimalRecords.DoesNotExist:
            return None

    def get(self, request, pk):
        animal = self.get_object(pk)
        if animal:
            serializer = AnimalRecordsSerializer(animal)
            return Response(serializer.data)
        return Response({"error": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        animal = self.get_object(pk)
        if animal:
            serializer = AnimalRecordsSerializer(
                animal, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)

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


class AnimalListView(APIView):
    schema = CustomSchema()
    @swagger_auto_schema(
        responses={
            200: AnimalRecordsSerializer,
            404: openapi.Response("No Animal list"),
        },
    )
    def get(self, request):
        animal = AnimalRecords.objects.all()
        serializers = AnimalRecordsSerializer(animal, many=True)
        return Response(serializers.data)
