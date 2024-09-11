from rest_framework import serializers
from tender.models import Tender, Bid

class TenderSerializer(serializers.ModelSerializer):
    #creator_name = serializers.CharField(max_length=50)

    class Meta:
        model = Tender
        fields = ['name', 'description', 'serviceType', 'status', 'organizationId', 'creatorUsername']

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['name', 'description', 'status', 'tenderId', 'organizationId', 'creatorUsername']

