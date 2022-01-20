from django.db import models
from authentication.models import User
from product.models import Product


# Create your models here.
class VendorDetails(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    aadharNumber = models.CharField(max_length=50)
    panNumber = models.CharField(max_length=50)
    companyName = models.CharField(max_length=200)
    companyLogo = models.ImageField(upload_to='uploads/companyLogo/')
    gstNumber = models.CharField(max_length=200)
    aadharImage = models.ImageField(upload_to='uploads/aadharImage/')
    panImage = models.ImageField(upload_to='uploads/panImage/')
    vendorSign = models.ImageField(upload_to='uploads/vendorSign/')
    vendorApproveStatus = models.BooleanField(default=False)
    ProfileUpdatePermission = models.BooleanField(default=True)
    POS = models.BooleanField(default=False)


class POSDetails(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor_id = models.ForeignKey(VendorDetails, on_delete=models.CASCADE)
    activeStatus = models.BooleanField(default=True)


class SubscriptionPlan(models.Model):
    price = models.IntegerField(default=0)
    activeStatus = models.BooleanField(default=True)


class SubscriptionPlanPurchase(models.Model):
    price = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    orderID = models.CharField(max_length=200)
    transID = models.CharField(max_length=200)
    referUserID = models.IntegerField(default=0)
    videoStatus = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class RewordPointForUser(models.Model):
    percentage = models.IntegerField(default=0)
    activeStatus = models.BooleanField(default=True)


class MinimumOrderValueForUser(models.Model):
    value = models.IntegerField(default=0)
    activeStatus = models.BooleanField(default=True)


class ReferRewardsList(models.Model):
    user_id = models.IntegerField(default=0)
    register_user_id = models.IntegerField(default=0)
    parent_user_id = models.IntegerField(default=0)
    cashbackLevel = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    cashbackStatus = models.BooleanField(default=False)
