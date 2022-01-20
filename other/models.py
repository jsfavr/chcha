from django.db import models
from authentication.models import User
from product.models import Product


# Create your models here.
class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    booking_id = models.IntegerField(default=0)
    ratting = models.IntegerField(default=0)
    details = models.CharField(max_length=500)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='uploads/subcategory/', default=0)


class Subscribe(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class InventoryTransaction(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    afterTransactionQuantity = models.IntegerField(default=0)
    remarks = models.CharField(max_length=100, null=True)
    transactionType = models.CharField(max_length=100, null=True)
    transactionID = models.CharField(max_length=100, null=True, default='')
    transactionDate = models.DateTimeField(auto_now_add=True)


class NotifyMe(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    emailID = models.EmailField(max_length=255)


class Settings(models.Model):
    coupon = models.BooleanField(default=False)
    debug = models.BooleanField(default=False)
    underMantanance = models.BooleanField(default=False)
    livePaymentGateway = models.BooleanField(default=False)
    vendorRegistration = models.BooleanField(default=True)
    appUpdateMandetory = models.BooleanField(default=False)
    acceptOrder = models.BooleanField(default=False)


class paymentOption(models.Model):
    gatewayName = models.CharField(max_length=100, null=True)
    live_key_secret = models.CharField(max_length=100, null=True)
    live_merchant_Key = models.CharField(max_length=100, null=True)
    test_key_secret = models.CharField(max_length=100, null=True)
    test_merchant_Key = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)


class shiprocketToken(models.Model):
    token = models.TextField(max_length=5000, null=True)
