from rest_framework import serializers
from tender.models import Tender, Bid

class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = ['id', 'name', 'description', 'service_type','status', 'organization_id', 'creator_id']

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'name', 'description', 'status', 'tender_id', 'organization_id', 'creator_id']

