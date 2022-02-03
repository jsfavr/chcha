from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, views
from rest_framework import permissions, status
from rest_framework.response import Response
from product.models import Product, ProductBrand, ProductImage
from django.core import serializers
from product.permissions import IsOwner
from booking.models import Booking
from category.models import SubCategory
from wallet.models import Wallet,WalletTransaction
import json
from django.db.models import Count

# Create your views here.
class shopPageAPIView(ListCreateAPIView):
    def post(self,request):
        inputs = request.data
        filterCategory=[]
        
        product=Product.objects.filter(adminActiveStatus=1,vendorActiveStatus=1)
        if int(inputs['cat'])!=0:
            product=product.filter(cat_id=inputs['cat'])
        if int(inputs['subCat'])!=0:
            product=product.filter(sub_cat_id_id=inputs['subCat'])
        if int(inputs['subSubCat'])!=0:
            product=product.filter(sub_sub_cat_id_id=inputs['subSubCat'])
        # if int(inputs['brand'])!=0:
        #     product=product.filter(productBrandID_id=inputs['brand'])
        print((inputs['productName']))
        print(len(inputs['productName']))
        if len(inputs['productName'])>1:
            product=product.filter(productName__contains=inputs['productName'])

       
        brandDetails=product
        brand=[]
        for eachProduct in brandDetails:
            brand1=ProductBrand.objects.filter(id=eachProduct.productBrandID_id)
            for eachBrand in brand1:
                newBrand = {
                    "id":eachBrand.id,
                    "name":eachBrand.brand_name
                }
            brand.append(newBrand)
        
        print(product.values('size').aggregate())
        sizeDetails=product
        size=[]
        for eachSize in sizeDetails:
            if eachSize.size!='NO':
                newSize = {
                    "size":eachSize.size,
                }
                size.append(newSize)

        colorDetails=product
        color=[]
        for eachColor in colorDetails:
            if eachColor.color!='NO':
                newColor = {
                    "color":eachColor.color,
                }
                color.append(newColor)





        filterCategory={
            "brand":brand,
            "size":size,
            "color":color,
        }

        return Response(filterCategory)
 

class AllShopAPIView(views.APIView):
    def post(self,request):
        inputs = request.data
        product=Product.objects.filter(adminActiveStatus=1,vendorActiveStatus=1)
        if int(inputs['cat'])!=0:
            product=product.filter(cat_id=inputs['cat'])
        if int(inputs['subCat'])!=0:
            product=product.filter(sub_cat_id_id=inputs['subCat'])
        if int(inputs['subSubCat'])!=0:
            product=product.filter(sub_sub_cat_id_id=inputs['subSubCat'])
        # if int(inputs['brand'])!=0:
        #     product=product.filter(productBrandID_id=inputs['brand'])
        if len(inputs['productName'])>1:
            product=product.filter(productName__contains=inputs['productName'])

        if len(inputs['brand'])!=0:
            product=product.filter(productBrandID_id__in=inputs['brand'])
        if len(inputs['size'])!=0:
            product=product.filter(size__in=inputs['size'])    
        if len(inputs['color'])!=0:
            product=product.filter(color__in=inputs['color'])
        if len(inputs['ratting'])!=0:
            product=product.filter(avgReview__gte=float(min(inputs['ratting'])))   
        if inputs['minPrice']!=0 or inputs['maxPrice']!=25000:
            product=product.filter(mrp__gte=inputs['minPrice'],mrp__lte=inputs['maxPrice'])      
        if int(inputs['sorting'])!=0:
            if int(inputs['sorting'])==1:
                 product=product.order_by('-id')
            if int(inputs['sorting'])==2:
                 product=product.order_by('-viewCount')
            if int(inputs['sorting'])==3:
                 product=product.order_by('-avgReview')
            if int(inputs['sorting'])==4:
                 product=product.order_by('avgReview')
            if int(inputs['sorting'])==5:
                 product=product.order_by('sellingPrice')
            if int(inputs['sorting'])==6:
                 product=product.order_by('-sellingPrice')   
        modifiedrel=[]
        for eachrel in product:
            det= Product.objects.filter(id=eachrel.id)
            image122 = ProductImage.objects.filter(productID_id=eachrel.id)
            brandddd = ProductBrand.objects.filter(id=eachrel.productBrandID_id)
            brand = ProductBrand.objects.values('brand_name').annotate(dcount=Count('brand_name')).filter(id=eachrel.productBrandID_id)
            subcatdel = SubCategory.objects.filter(id=eachrel.sub_cat_id_id)
            relDetails = serializers.serialize('json', det)
            relImage = serializers.serialize('json', image122)
            relbrand = serializers.serialize('json', brandddd)
            relsub = serializers.serialize('json', subcatdel)
            newrel = {
                'rel' : relDetails,
                'image' : relImage,
                'brand' : relbrand,
                'sub': relsub,
                'pband':brand
            }
            modifiedrel.append(newrel)
        return Response(modifiedrel)