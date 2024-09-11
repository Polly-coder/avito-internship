# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Employee(models.Model):
    username = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee'


class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organization'


class OrganizationResponsible(models.Model):
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organization_responsible'

# убрать
'''
class TenderStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        db_table = 'tender_status'
 '''   

class Tender(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    #service_type = models.CharField(max_length=50) #"Construction",
    serviceType = models.CharField(max_length=50)
    #status = models.ForeignKey(TenderStatus, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    #organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    organizationId = models.ForeignKey(Organization, on_delete=models.CASCADE)
    #creator_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    creatorUsername = models.CharField(max_length=50)
    #"creatorUsername": "user1" по юзернейму находим пользователя и дабавляем id

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        db_table = 'tender'

# убрать
'''
class BidStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        db_table = 'bid_status'
'''

class Bid(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    #status = models.ForeignKey(BidStatus, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    #tender_id = models.ForeignKey(Tender, on_delete=models.CASCADE)
    tenderId = models.ForeignKey(Tender, on_delete=models.CASCADE)
    #organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    organizationId = models.ForeignKey(Organization, on_delete=models.CASCADE)
    #creator_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    creatorUsername = models.CharField(max_length=50)
    #"creatorUsername": "user1" по юзернейму находим пользователя и дабавляем id

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        db_table = 'bid'
    
class Review(models.Model):
    description = models.TextField()
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    bid_id = models.ForeignKey(Bid, on_delete=models.CASCADE)
    creator_id = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        db_table = 'review'
