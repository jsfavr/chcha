from django.db import models


# Create your models here.
class Coupon(models.Model):
    title = models.CharField(max_length=300, null=True)
    discount = models.IntegerField(default=0)
    couponImage = models.ImageField(upload_to='uploads/couponImage/')
    couponCode = models.CharField(max_length=100, unique=True)
    couponType = models.CharField(max_length=50)
    activeStatus = models.BooleanField(default=True)
    couponValidDate = models.DateField(null=True)
    minPrice = models.IntegerField(default=0)

class DisplayBanner(models.Model):
    image = models.ImageField(upload_to='uploads/displayBanner/')
class PromotionBanner(models.Model):
    image = models.ImageField(upload_to='uploads/promotionBanner/')
    url = models.CharField(max_length=300, null=True)