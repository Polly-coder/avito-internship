from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  status
from tender.serializers import TenderSerializer, BidSerializer

# Create your views here.

class PingView(APIView):
    def get(self, request):
        return Response('ok')

class TenderNewView(APIView):
    def post(self, request):
        data = request.data
        serializer = TenderSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                data   = serializer.error,
                status = 400
            )
        serializer.save()
        return Response(
                data   = serializer.data,
                status = 200
            )

