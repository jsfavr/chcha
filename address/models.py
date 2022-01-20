from django.db import models
from authentication.models import User


# Create your models here.
class ShippingAddress(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)
    flat = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=300, null=True)
    location = models.CharField(max_length=150, null=True)
    landmark = models.CharField(max_length=150, null=True, default='na')
    city = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=10)
    optionalPhone = models.CharField(max_length=10, null=True)


class BillingAddress(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)
    flat = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=300, null=True)
    location = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)


class DeliveryPincode(models.Model):
    pincode = models.CharField(max_length=6, unique=True)
    minPrice = models.IntegerField(default=0)
    deliveryCharge = models.IntegerField(default=0)
    cod = models.CharField(default='YES', max_length=100)
    activeStatus = models.BooleanField(default=True)


class DeliveryBoyPincode(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)
    activeStatus = models.BooleanField(default=True)
