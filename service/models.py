from django.db import models
from authentication.models import User
from product.models import Product
from address.models import ShippingAddress
import datetime

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to='uploads/service/')
    tagLing = models.CharField(max_length=100,null=True)
    description = models.TextField(max_length=1000,null=True)
    price = models.IntegerField(default=0)
    mrp = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    activeStatus = models.BooleanField(default=True)
    vendoractiveStatus = models.BooleanField(default=True)


class Enquiry(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.TextField(max_length=255, null=True)
    date =models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

