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
        #Employee.objects.filter(username=user_name)
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
        limit = int(request.GET.get('limit', 5)) # или по дефолту все?
        offset = int(request.GET.get('offset', 0))
        service_type = request.GET.get('service_type', None)
        if service_type:
            tenders = Tender.objects.filter(serviceType__in = service_type)[offset:limit]
        else: tenders = Tender.objects.all()[offset:limit]
        serializer_for_tenders = TenderSerializer(instance = tenders, many = True)
        return Response(serializer_for_tenders.data)
    
class MyTenderView(APIView):
    def get(self, request):
        limit = int(request.GET.get('limit', 5))
        offset = int(request.GET.get('offset', 0))
        user_name = request.GET.get('username', None)
        
        if Employee.objects.filter(username=user_name):
            tenders = Tender.objects.filter(creatorUsername = user_name)[offset:limit]
        else:
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        serializer_for_tenders = TenderSerializer(instance = tenders, many = True)
        return Response(serializer_for_tenders.data)
    
class BidNewView(APIView):
    def post(self, request):
        serializer = BidSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data   = serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
        if not Employee.objects.filter(username=serializer.validated_data['creatorUsername']).exists():
            return Response(
                data   = 'Пользователь не существует или некорректен',
                status = 401
            )
        
        serializer.save()
        return Response(
                data   = serializer.data,
                status = 200
            )

class MyBidView(APIView):
    def get(self, request):
        limit = int(request.GET.get('limit', 5))
        offset = int(request.GET.get('offset', 0))
        user_name = request.GET.get('username', None)
        
        if Employee.objects.filter(username=user_name):
            bids = Bid.objects.filter(creatorUsername = user_name)[offset:limit]
        else:
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        serializer_for_bids = BidSerializer(instance = bids, many = True)
        return Response(serializer_for_bids.data)
    
class BidsByTenderView(APIView):
    def get(self, request, pk):
        limit = int(request.GET.get('limit', 5))
        offset = int(request.GET.get('offset', 0))
        user_name = request.GET.get('username')

        if Employee.objects.filter(username=user_name):
            if Tender.objects.filter(id=pk):
                bids = Bid.objects.filter(creatorUsername = user_name, tenderId = pk)[offset:limit]
            else:
                return Response({'reason':'Тендер не существует или id некорректен'}, 400)
        else:
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        
        serializer_for_bids = BidSerializer(instance = bids, many = True)
        return Response(serializer_for_bids.data)