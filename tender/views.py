from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  status
from tender.serializers import TenderSerializer, BidSerializer
from tender.models import Tender, Bid, Employee, Organization

# Create your views here.

class PingView(APIView):
    def get(self, request):
        return Response('ok')

class TenderNewView(APIView):
    def post(self, request):
        data = request.data
        serializer = TenderSerializer(data=data)
        users = Employee.objects.all()
        if not serializer.is_valid():
            return Response(
                data   = serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        for user in users:
            if user.username == serializer.validated_data['creatorUsername']:
                break
        else:
            return Response(
                data   = 'Пользователь не существует или некорректен',
                status = 401
            )
        
        #serializer.save(creator_id = userId)
        serializer.save()
        return Response(
                data   = serializer.data,
                status = 200
            )

class TenderView(APIView):
    def get(self, request):
        pass

