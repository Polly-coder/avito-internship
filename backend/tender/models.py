from django.db import models

# Create your models here.

class Employee(models.Model):
    # id задаётся django по умолчанию SERIAL PRIMARY KEY,
    username = models.CharField(max_length=50, unique=True) #VARCHAR(50) UNIQUE NOT NULL,
    first_name = models.CharField(max_length=50, null=True) #VARCHAR(50),
    last_name = models.CharField(max_length=50, null=True) #VARCHAR(50),
    created_at = models.DateTimeField(auto_now_add=True) #TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at = models.DateTimeField(auto_now_add=True) #TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    def __str__(self) -> str:
        return str(self.name)


class Organization(models.Model):
    ORGANIZATION_CHOICES = (
        (IE, 'IE'),
        (LLC, 'LLC'),
        (JSC, 'JSC')
    )
    #id SERIAL PRIMARY KEY,
    name = models.CharField(max_length=100) #VARCHAR(100) NOT NULL,
    description = models.TextField() #TEXT,
    organization_type = models.IntegerField(choices=ORGANIZATION_CHOICES)
    created_at  = models.DateTimeField(auto_now_add=True) #TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at = models.DateTimeField(auto_now_add=True) #TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    def __str__(self) -> str:
        return str(self.name)

class Organization_responsible(models.Model):
    #id SERIAL PRIMARY KEY,
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE) #INT REFERENCES organization(id) ON DELETE CASCADE,
    user_id = models.ForeignKey(Employee, on_delete=models.CASCADE) #INT REFERENCES employee(id) ON DELETE CASCADE

class TenderStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)

class Tender(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    service_type = models.CharField(max_length=50) #"Construction",
    status = models.ForeignKey(TenderStatus, on_delete=models.CASCADE)
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    creator_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    #"creatorUsername": "user1" по юзернейму находим пользователя и дабавляем id

    def __str__(self) -> str:
        return str(self.name)

class BidStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)


class Bid(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    status = models.ForeignKey(BidStatus, on_delete=models.CASCADE)
    tender_id = models.ForeignKey(Tender, on_delete=models.CASCADE)
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    creator_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    #"creatorUsername": "user1" по юзернейму находим пользователя и дабавляем id

    def __str__(self) -> str:
        return str(self.name)
    
class Review(models.Model):
    description = models.TextField()
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    bid_id = models.ForeignKey(Bid, on_delete=models.CASCADE)
    creator_id = models.ForeignKey(Employee, on_delete=models.CASCADE)