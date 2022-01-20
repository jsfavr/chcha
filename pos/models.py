from django.db import models
from authentication.models import User
from product.models import Product
from datetime import timedelta

# Create your models here.
class POSCART(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class POSBooking(models.Model):
    orderID = models.CharField(max_length=20,default=0)
    grandTotal = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    date = models.DateField(auto_now=True)
    posID = models.ForeignKey(User, on_delete=models.CASCADE)

class POSBookingItem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    productSellingPrice = models.IntegerField(default=0)
    productTotalPrice = models.IntegerField(default=0)
    Status = models.BooleanField(default=False)
    POSBookingID = models.ForeignKey(POSBooking, on_delete=models.CASCADE)
   


