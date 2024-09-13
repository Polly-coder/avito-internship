# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinValueValidator
import uuid 


class Employee(models.Model):
    id = models.UUIDField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee'


class Organization(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organization'


class OrganizationResponsible(models.Model):
    id = models.UUIDField(primary_key=True)
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organization_responsible'
 

class Tender(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    serviceType = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default = 'Created')
    organizationId = models.ForeignKey(Organization, on_delete=models.CASCADE)
    version = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    createdAt = models.DateTimeField(auto_now_add=True)
    creatorUsername = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        db_table = 'tender'


class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=50, default = 'Created')
    tenderId = models.ForeignKey(Tender, on_delete=models.CASCADE)
    #organizationId = models.ForeignKey(Organization, on_delete=models.CASCADE)
    authorType = models.CharField(max_length=50)
    authorId = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)
    #authorId = models.UUIDField(null=False)
    version = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    createdAt = models.DateTimeField(auto_now_add=True)
    #creatorUsername = models.CharField(max_length=50)
    bidDecision = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        db_table = 'bid'
    
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    description = models.TextField()
    #organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    bidId = models.ForeignKey(Bid, on_delete=models.CASCADE)
    #creator_id = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        db_table = 'review'
