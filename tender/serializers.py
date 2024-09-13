from rest_framework import serializers
from tender.models import Tender, Bid

class TenderSerializer(serializers.ModelSerializer):
    #creator_name = serializers.CharField(max_length=50)
    creatorUsername = serializers.CharField(max_length = 50)
    class Meta:
        model = Tender
        #fields = ['name', 'description', 'serviceType', 'status', 'organizationId', 'creatorUsername']
        fields = ['id', 'name', 'description', 'serviceType', 'status', 'organizationId', 'version', 'createdAt', 'creatorUsername']

class BidSerializer(serializers.ModelSerializer):
    #creatorUsername = serializers.CharField(max_length = 50)
    class Meta:
        model = Bid
        fields = ['id', 'name', 'description', 'status', 'tenderId', 'authorType', 'authorId', 'version', 'createdAt']

