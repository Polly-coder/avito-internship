from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  status
from tender.serializers import TenderSerializer, BidSerializer
from tender.models import Tender, Bid, Employee, Organization, OrganizationResponsible
from uuid import UUID

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
    
class TenderStatusView(APIView):
    def get(self, request, pk):
        user_name = request.GET.get('username')
        try:
            uuid_obj = UUID(pk, version=4)
        except ValueError:
            return Response({'reason':'uuid некорректен'}, 400)
        
        tender_obj = Tender.objects.filter(id=uuid_obj).first()

        if not Employee.objects.filter(username=user_name).exists():
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        if not tender_obj:
            return Response({'reason':'Тендер не существует или uuid некорректен'}, 400)
        if tender_obj.creatorUsername != user_name:
            return Response({'reason':'Недостаточно прав для выполнения действия'}, 403)
        return Response(tender_obj.status)
    
    def put(self, request, pk):
        available_statuses = ['Created', 'Published', 'Closed']
        status = request.GET.get('status')
        user_name = request.GET.get('username')

        if not status in available_statuses:
            return Response({'reason':'Статус некорректен, возможные статусы: Created, Published, Closed'}, 400)
        try:
            uuid_obj = UUID(pk, version=4)
        except ValueError:
            return Response({'reason':'uuid некорректен'}, 400)
        
        tender_obj = Tender.objects.filter(id=uuid_obj).first()

        if not Employee.objects.filter(username=user_name).exists():
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        if not tender_obj:
            return Response({'reason':'Тендер не существует или uuid некорректен'}, 400)
        if tender_obj.creatorUsername != user_name:
            return Response({'reason':'Недостаточно прав для выполнения действия'}, 403)
        
        data = {
            "status": status,
        }
        serializer = TenderSerializer(instance=tender_obj, data = data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(status=status)
            return Response(serializer.data)
        else:
            return Response({'reason':'Данные некорректны'}, 400)
        
class TenderEditView(APIView):
    def patch(self, request, pk):
        user_name = request.GET.get('username')

        try:
            uuid_obj = UUID(pk, version=4)
        except ValueError:
            return Response({'reason':'uuid некорректен'}, 400)
        
        tender_obj = Tender.objects.filter(id=uuid_obj).first()

        if not Employee.objects.filter(username=user_name).exists():
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        if not tender_obj:
            return Response({'reason':'Тендер не существует или uuid некорректен'}, 400)
        if tender_obj.creatorUsername != user_name:
            return Response({'reason':'Недостаточно прав для выполнения действия'}, 403)
        
        serializer = TenderSerializer(instance=tender_obj, data = request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(version=tender_obj.version+1)
            return Response(serializer.data)
        else:
            return Response({'reason':'Данные некорректны'}, 400)
'''
OLD VERSION
-----
class BidNewView(APIView):
    def post(self, request):
        serializer = BidSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data   = serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        user = Employee.objects.filter(username=serializer.validated_data['creatorUsername']).first()
        #org_user = OrganizationResponsible.objects.filter(user=user).first()
        if not user:
            return Response(
                data   = 'Пользователь не существует или некорректен',
                status = 401
            )
        author_id = user
        serializer.save(authorId=author_id)
        return Response(
                data   = serializer.data,
                status = 200
            )
'''   
class BidNewView(APIView):
    def post(self, request):
        serializer = BidSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data   = serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        if not serializer.validated_data['authorType'] in ('User', 'Organization'):
            return Response({'reason':'Некорректный тип автора'}, 400)
        
        author_id = serializer.validated_data['authorId'].id
        '''
        try:
            uuid_obj = UUID(author_id, version=4)
        except ValueError:
            return Response({'reason':'uuid автора некорректен'}, 400)
        '''
        user = Employee.objects.filter(id=author_id).first()
        if not user:
            return Response({'reason':'Пользователь не существует или некорректен'}, 401)
    
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
        user = Employee.objects.filter(username=user_name).first()
        if not user:
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        #org_user = OrganizationResponsible.objects.filter(user = user.id).first()
        bids = Bid.objects.filter(authorId = user) 
        #if not org_user:
        #    return Response({'reason':'Пользователь не привязан к организации'}, 200)
        #| Bid.objects.filter(authorId = org_user.organization.id)
            
        serializer_for_bids = BidSerializer(instance = bids[offset:limit], many = True)
        return Response(serializer_for_bids.data)
    
class BidsByTenderView(APIView):
    def get(self, request, pk):
        limit = int(request.GET.get('limit', 5))
        offset = int(request.GET.get('offset', 0))
        user_name = request.GET.get('username')
                  
        try:
            uuid_obj = UUID(pk, version=4)
        except ValueError:
            return Response({'reason':'uuid некорректен'}, 400)

        if not Employee.objects.filter(username=user_name).exists():
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        if not Tender.objects.filter(id=uuid_obj).exists():
            return Response({'reason':'Тендер не существует или id некорректен'}, 400)
        bids = Bid.objects.filter(tenderId = pk)[offset:limit]
        
        serializer_for_bids = BidSerializer(instance = bids, many = True)
        return Response(serializer_for_bids.data)
    
class BidStatusView(APIView):
    def get(self, request, pk):
        user_name = request.GET.get('username')
        try:
            uuid_obj = UUID(pk, version=4)
        except ValueError:
            return Response({'reason':'uuid некорректен'}, 400)
        
        bid_obj = Bid.objects.filter(id=uuid_obj).first()
        user = Employee.objects.filter(username=user_name).first()
        #org_user = OrganizationResponsible.objects.filter(user = user).first()
        if not Employee.objects.filter(username=user_name).exists():
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        if not bid_obj:
            return Response({'reason':'Предложение не существует или uuid некорректен'}, 400)
        if bid_obj.authorId != user:
            return Response({'reason':'Недостаточно прав для выполнения действия'}, 403)
        return Response(bid_obj.status)
    
    def put(self, request, pk):
        available_statuses = ['Created', 'Published', 'Canceled']
        status = request.GET.get('status')
        user_name = request.GET.get('username')

        if not status in available_statuses:
            return Response({'reason':f'Статус некорректен, возможные статусы: {' '.join(available_statuses)}'}, 400)
        try:
            uuid_obj = UUID(pk, version=4)
        except ValueError:
            return Response({'reason':'uuid некорректен'}, 400)
        
        bid_obj = Bid.objects.filter(id=uuid_obj).first()
        user = Employee.objects.filter(username=user_name).first()
        if not user:
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        if not bid_obj:
            return Response({'reason':'Предложение не существует или uuid некорректен'}, 400)
        if bid_obj.authorId != user:
            return Response({'reason':'Недостаточно прав для выполнения действия'}, 403)
        
        data = {
            "status": status,
        }
        serializer = BidSerializer(instance=bid_obj, data = data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(status=status)
            return Response(serializer.data)
        else:
            return Response({'reason':'Данные некорректны'}, 400)
        
class BidEditView(APIView):
    def patch(self, request, pk):
        user_name = request.GET.get('username')

        try:
            uuid_obj = UUID(pk, version=4)
        except ValueError:
            return Response({'reason':'uuid некорректен'}, 400)
        
        bid_obj = Bid.objects.filter(id=uuid_obj).first()
        user = Employee.objects.filter(username=user_name).first()
        if not user:
            return Response({'reason':'Пользователь не существует или некорректен'}, 400)
        if not bid_obj:
            return Response({'reason':'Предложение не существует или uuid некорректен'}, 400)
        if bid_obj.authorId != user:
            return Response({'reason':'Недостаточно прав для выполнения действия'}, 403)
        
        serializer = BidSerializer(instance=bid_obj, data = request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(version=bid_obj.version+1)
            return Response(serializer.data)
        else:
            return Response({'reason':'Данные некорректны'}, 400)