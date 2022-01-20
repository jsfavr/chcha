from django.db import models
from authentication.models import User
from category.models import Category, SubCategory, SubSubCategory


# Create your models here.
class ProductBrand(models.Model):
    brand_name = models.CharField(max_length=50)
    brand_logo = models.ImageField(upload_to='uploads/brand/')


class ProductGroup(models.Model):
    group_name = models.CharField(max_length=50)


class Product(models.Model):
    productCode = models.CharField(max_length=50)
    skuCode = models.CharField(max_length=50)
    productGroupID_id = models.IntegerField(default=0)
    productBrandID_id = models.IntegerField(default=0)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    sub_cat_id = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    sub_sub_cat_id = models.ForeignKey(
        SubSubCategory, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    productName = models.CharField(max_length=200)
    productDescription = models.CharField(
        max_length=2000, null=True, blank=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(max_length=200, null=True, blank=True)
    mrp = models.IntegerField(default=1)
    sellingPrice = models.DecimalField(
        default=1.0, decimal_places=10, max_digits=20)
    totalReview = models.IntegerField(default=0)
    avgReview = models.DecimalField(
        max_digits=2, decimal_places=1, default=0.0)
    viewCount = models.IntegerField(default=0)
    vendorActiveStatus = models.BooleanField(default=True)
    adminActiveStatus = models.BooleanField(default=True)
    totalStock = models.IntegerField(default=0)
    availableStock = models.IntegerField(default=0)
    orderCount = models.IntegerField(default=0)
    contryOfOrigin = models.CharField(max_length=50, null=True, blank=True)


class ProductImage(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    productImage = models.ImageField(upload_to='uploads/productImage/')


class ProductFeature(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.CharField(max_length=500)


class ProductSpecification(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    details = models.CharField(max_length=500)
