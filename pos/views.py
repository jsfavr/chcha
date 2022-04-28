from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, views
from rest_framework import permissions, status
from .models import POSCART, POSBooking, POSBookingItem
from rest_framework.response import Response
from product.models import Product, ProductBrand, ProductImage
from django.core import serializers
from product.permissions import IsOwner
from booking.models import Booking
from category.models import SubCategory
from wallet.models import Wallet,WalletTransaction
from django.db.models import Sum, Count
from authentication.models import User
from datetime import date
from django.db.models.functions import ExtractYear, ExtractMonth
from other.models import InventoryTransaction
from userDetails.models import VendorDetails,POSDetails

# Create your views here.
class POSAllProductDeleteAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        user_id=self.request.user.id
        POSCART.objects.filter(user_id_id=user_id).delete()
        print(user_id)
        newrel = {
                'status':'Delete Successfull'
            }
        return Response(newrel)

class addToCartAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        user_id=int(self.request.user.id)
        inputs=request.data
        prod=Product.objects.filter(productCode=inputs['product_code'])
        for eachProd in prod :
            id=eachProd.id
            qqty=eachProd.availableStock
        

        if qqty>0:
            pos=POSCART.objects.filter(product_id_id=id,user_id_id=user_id)
            if pos:
                for eachpos in pos :
                    qty=eachpos.quantity
                if qty>qqty:
                    newrel = {
                        'status':2
                    }
                else :
                   POSCART.objects.filter(product_id_id=id,user_id_id=user_id).update(quantity=qty+1)
                   newrel = {
                        'status':1
                    }
            else :
                POSCART.objects.create(product_id_id=id,user_id_id=user_id,quantity=1)
                newrel = {
                    'status':1
                }
        else :
             newrel = {
                'status':0
            }


        

       
        return Response(newrel)

class GetProductAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        user_id=int(self.request.user.id)
        productArray=[]
        total=0
        prod3=POSCART.objects.filter(user_id_id=user_id)
        for eachProd3 in prod3:
            product=Product.objects.filter(id=eachProd3.product_id_id)
            for eachProd in product:
                brand=ProductBrand.objects.filter(id=eachProd.productBrandID_id)
                for eachbrand in brand:
                    brandName=eachbrand.brand_name
                image=ProductImage.objects.filter(productID_id=eachProd.id)[:1]
                for eachimage in image:
                    productImage=eachimage.productImage
                sub=SubCategory.objects.filter(id=eachProd.sub_cat_id)
                for eachsub in sub:
                    gst=eachsub.gst
                id=eachProd.id
                name=eachProd.productName
                mrp=eachProd.mrp
                code=eachProd.productCode

                sellingPrice=eachProd.sellingPrice+((eachProd.sellingPrice*gst)/100)
            total=total+(eachProd3.quantity*sellingPrice)
            newrel = {
                'id' : id,
                'name' : name,
                'brand' : brandName,
                'productImage' : str(productImage),
                'mrp' : mrp,
                'sellingPrice' : sellingPrice,
                'code' : code,
                'qty': eachProd3.quantity,
               
            }

            productArray.append(newrel)
        ac = {
            'productArray':productArray,
            'total':round(total)
        }
        return Response(ac)


class OrderSubmitAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        user_id=int(self.request.user.id)
        productArray=[]
        total=0
        inputs=request.data
        bok=POSBooking.objects.create(
                orderID=inputs['orderID'],
                grandTotal=inputs['grandTotal'],
                name=inputs['name'],
                phone=inputs['phone'],
                posID_id=user_id
            )
        prod3=POSCART.objects.filter(user_id_id=user_id)
        for eachProd3 in prod3:
            product=Product.objects.filter(id=eachProd3.product_id_id)
            for eachProd in product:
                availableStock=eachProd.availableStock
                orderCount=eachProd.orderCount
                id=eachProd.id
                sub=SubCategory.objects.filter(id=eachProd.sub_cat_id)
                for eachsub in sub:
                    gst=eachsub.gst
                sellingPrice=eachProd.sellingPrice+((eachProd.sellingPrice*gst)/100)
                print(eachProd.id)
                
              
                sub=SubCategory.objects.filter(id=eachProd.sub_cat_id)
                for eachsub in sub:
                    gst=eachsub.gst
                
            POSBookingItem.objects.create(
                product_id_id=id,
                quantity=eachProd3.quantity,
                productSellingPrice=sellingPrice,
                productTotalPrice=sellingPrice*eachProd3.quantity,
                POSBookingID_id=bok.id
            )
            Product.objects.filter(id=id).update(availableStock=availableStock-eachProd3.quantity,orderCount=orderCount+1)
            InventoryTransaction.objects.create(product_id_id=id,quantity=eachProd3.quantity,remarks='POS Booking',transactionType='DEBIT',transactionID='',afterTransactionQuantity=availableStock-eachProd3.quantity)
        POSCART.objects.filter(user_id_id=user_id).delete()
        ac = {
            'status' : 'Booking Successfull',
            'code' : 1,
        }
        return Response(ac)



class OrderViewAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        user_id=int(self.request.user.id)
        bookingArray=[]
        booking=POSBooking.objects.filter(posID_id=user_id).order_by('-id')
        for eachBooking in booking:
            newrel = {
                'id':eachBooking.id,
                'name':eachBooking.name,
                'phone':eachBooking.phone,
                'price':eachBooking.grandTotal,
                'date':eachBooking.date,
                'orderID':eachBooking.orderID,
            }
            bookingArray.append(newrel)
        return Response(bookingArray)

class OrderViewVendorAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        user_id=int(self.request.user.id)
        bookingArray=[]
        vendorDetail=VendorDetails.objects.filter(user_id_id=user_id)
        for eachvendorDetail in vendorDetail:
            vendorDetailID=eachvendorDetail.id
        
        posDetail=POSDetails.objects.filter(vendor_id_id=vendorDetailID)
        for eachposDetail in posDetail:
            posID=eachposDetail.user_id_id


        booking=POSBooking.objects.filter(posID_id=posID).order_by('-id')
        for eachBooking in booking:
            newrel = {
                'id':eachBooking.id,
                'name':eachBooking.name,
                'phone':eachBooking.phone,
                'price':eachBooking.grandTotal,
                'date':eachBooking.date,
                'orderID':eachBooking.orderID,
            }
            bookingArray.append(newrel)
        return Response(bookingArray)

class OrderViewDetailsAPIView(views.APIView):
    def post(self,request):
        bookingArray=[]
        productArray=[]
        inputs=request.data
        booking=POSBooking.objects.filter(id=inputs['id'])
        for eachBooking in booking:
            newrel = {
                'id':eachBooking.id,
                'name':eachBooking.name,
                'phone':eachBooking.phone,
                'price':eachBooking.grandTotal,
                'date':eachBooking.date,
                'orderID':eachBooking.orderID,
            }
        productBooking=POSBookingItem.objects.filter(POSBookingID=inputs['id'])
        for eachproductBooking in productBooking:
            product=Product.objects.filter(id=eachproductBooking.product_id_id)
            for eachProduct in product:
                newrel2 = {
                    'id':eachproductBooking.product_id_id,
                    'productCode':eachProduct.productCode,
                    'name':eachProduct.productName,
                    'size':eachProduct.size,
                    'color':eachProduct.color,
                    'quantity':eachproductBooking.quantity,
                    'productSellingPrice':eachproductBooking.productSellingPrice,
                    'productTotalPrice':eachproductBooking.productTotalPrice,
                }
                productArray.append(newrel2)

        abc = {
            'productDetail':productArray,
            'details':newrel
        }
        return Response(abc)



