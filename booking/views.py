from typing import Generator
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import BookingSerializer, ReasonSerializer
from product.permissions import IsOwner
from rest_framework import permissions, views, status
from .models import Booking, Reason, BookingPayment
from product.models import Product, ProductBrand, ProductImage
from category.models import SubCategory
from wallet.models import Wallet, WalletTransaction
from rest_framework.response import Response
from django.core import serializers
from address.models import ShippingAddress, BillingAddress
from datetime import datetime
from other.models import InventoryTransaction
from authentication.models import User
from userDetails.models import VendorDetails
from django.conf import settings
from authentication.utils import Util
import requests
from django.db.models import Q, Sum
from wallet.views import smsSend
import math
from datetime import date
import shortuuid
import json
# Create your views here.


class BookingAPIView(ListCreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class BookingAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


# Create your views here.
class ReasonAPIView(ListCreateAPIView):
    serializer_class = ReasonSerializer
    queryset = Reason.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class ReasonAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReasonSerializer
    queryset = Reason.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class userBookingAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        user_id = self.request.user.id

        booking2 = []
        ShippingAddressDetails = []
        booking = Booking.objects.filter(user_id_id=user_id).order_by('-id')
        for eachbooking in booking:

            bookingDetails = {
                'OrderID': eachbooking.orderID,
                'orderDate': eachbooking.OrderDate,
                'productPayablePrice': eachbooking.productPayablePrice,
                'productSellingPrice': eachbooking.productSellingPrice,
                'productGST': eachbooking.productGST,
                'deliveryCharge': eachbooking.deliveryCharge,
                'walletAmount': eachbooking.walletAmount,
                'couponDiscount': eachbooking.couponDiscount	,
                'couponCode': eachbooking.couponCode,
                'orderStatus': eachbooking.orderStatus,
                'paymentType': eachbooking.paymentType,
                'razorpayPaymentId': eachbooking.razorpayPaymentId,
                'deliveryDate': eachbooking.deliveryDate,
                'returnDate': eachbooking.returnDate,
                'returnExpairStatus': eachbooking.returnExpairStatus,
                'orderInTransitDate': eachbooking.orderInTransitDate,
                'readyForReturnDate': eachbooking.readyForReturnDate,
                'cancelDate': eachbooking.cancelDate,
                'reviewStatus': eachbooking.reviewStatus,
                'booking_id': eachbooking.id,
                'qty': eachbooking.quantity

            }

            product = Product.objects.filter(id=eachbooking.product_id_id)
            for eachproduct in product:
                productName = eachproduct.productName
                Product_id = eachproduct.id
                ProductCode = eachproduct.productCode
                mrp = eachproduct.mrp
                sellingPrice = eachproduct.sellingPrice
                image122 = ProductImage.objects.filter(
                    productID_id=eachproduct.id)
                for eachimage in image122:
                    image = eachimage.productImage

                brand22 = ProductBrand.objects.filter(
                    id=eachproduct.productBrandID_id)
                for eachbrand in brand22:
                    Brand = eachbrand.brand_name
                subcatdel = SubCategory.objects.filter(
                    id=eachproduct.sub_cat_id_id)
                for eachsubcatdel in subcatdel:
                    gst = eachsubcatdel.gst
            productDetail = {
                'productID': Product_id,
                'productName': productName,
                'productCode': ProductCode,
                'brand': Brand,
                'image': str(image),
                'mrp': mrp,
                'sellingPrice': round(sellingPrice)

            }
            add = ShippingAddress.objects.filter(
                id=eachbooking.shippingAddressId_id)
            for eachadd in add:
                pincode = eachadd.pincode
                flat = eachadd.flat
                address = eachadd.address
                location = eachadd.location
                landmark = eachadd.landmark
                city = eachadd.city
                district = eachadd.district
                state = eachadd.state
                name = eachadd.name
                phone = eachadd.phone
                optionalPhone = eachadd.optionalPhone
            ShippingAddressDetails = {
                'pincode': pincode,
                'flat': flat,
                'address': address,
                'location': location,
                'landmark': landmark,
                'city': city,
                'district': district,
                'state': state,
                'name': name,
                'phone': phone,
                'optionalPhone': optionalPhone,
            }

            pro = {
                'bookingDetails': bookingDetails,
                'productDetail': productDetail,
                'shippingAddress': ShippingAddressDetails,
                'deliveryBoyName':eachbooking.deliveryBoyName,
                'deliveryBoyPhone':eachbooking.deliveryBoyPhone,
                'returnBoyName':eachbooking.returnBoyName,
                'returnBoyPhone':eachbooking.returnBoyPhone
            }
            booking2.append(pro)
        return Response(booking2)


class userCancelBookingAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        newrel = []
        user_id = self.request.user.id
        phone_no = self.request.user.phone
        email = self.request.user.email
        name = self.request.user.name
        user_details = User.objects.filter(id=user_id).first()
        inputs = request.data
        # print(inputs['booking_id'])
        eachbooking = Booking.objects.filter(id=inputs['booking_id']).first()
        if eachbooking.orderStatus!=9:
            productPayablePrice = eachbooking.productPayablePrice
            couponDiscount = eachbooking.couponDiscount
            walletPoint = eachbooking.walletPoint
            product_id = eachbooking.product_id_id
            qty = eachbooking.quantity
            bookingID = eachbooking.orderID

            wallet = Wallet.objects.filter(user_id_id=user_id).first()
            currentWalletBalance = wallet.amount

            RefundableAmount = productPayablePrice-couponDiscount-walletPoint
            updatedWalletBalance = currentWalletBalance+RefundableAmount

            bookingUpdate = Booking.objects.filter(id=inputs['booking_id']).update(
                orderStatus=9, cancelDate=datetime.now())
            print(eachbooking.paymentType)
            if eachbooking.paymentType!='Cash On Delivery':
                walletUpdate = Wallet.objects.filter(
                    user_id_id=user_id).update(amount=updatedWalletBalance)
                WalletTransCreate = WalletTransaction.objects.create(
                    user_id_id=user_id, transactionAmount=RefundableAmount, afterTransactionAmount=updatedWalletBalance, remarks='Cancel Order', transactionType='CREDIT')
            else:
                print('Cash On Delivery')
            
            reasonCreate = Reason.objects.create(
                user_id_id=user_id, booking_id_id=inputs['booking_id'], type='Cancel', reason=inputs['cancel_option'], message=inputs['cancel_msg'])

            product = Product.objects.filter(id=product_id)
            # productDetails=serializers.serialize('json', product)
            for eachProd in product:
                totalStock = int(eachProd.totalStock)+int(qty)
                availableStock = int(eachProd.availableStock)+int(qty)

            Product.objects.filter(id=product_id).update(
                totalStock=totalStock, availableStock=availableStock)

            product_trans_data = InventoryTransaction.objects.create(
                product_id_id=product_id, quantity=qty, remarks='Cancel Booking', transactionType='CREDIT', transactionID=bookingID, afterTransactionQuantity=availableStock)
            product_trans_data.save()

            newrel = {
                'status': 'Booking Canceled',
                'code': 1,
            }
            # sms_body = 'Booking Canceled : Hi, your order has been canceled as per your request.'
            # response = requests.get(
            #     "http://weberleads.in/http-tokenkeyapi.php?authentic-key=3134696e7374616e745f6765747761793631321586003895&senderid=INGWAY&route=2&number="+phone_no+"&message="+sms_body)
            # data = {'title': 'Booking Canceled', 'content': sms_body, 'email_subject': 'Booking Canceled',
            #         'to_email': user_details.email, 'from_email': settings.EMAIL_HOST_USERS}
            # Util.email_send(data)
            message = 'Booking Canceled : Hi, your order has been canceled as per your request.'
            template_id = ''
            # smsSend(phone_no, message, template_id)
            # data = {
            #     'name': name,
            #     'email': email,
            #     'subject': 'Booking Canceld',
            #     'message': 'Your order has been canceled as per your request.',
            #     'from_email': settings.EMAIL_HOST_USER
            # }
            # Util.email_send(data)
        else:
            newrel = {
                'status': 'Booking already Canceled',
                'code': 1,
            }
        return Response(newrel)


class vendorBookingAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, status):
        booking2 = []
        booking = []
        ShippingAddressDetails = []
        user_id = self.request.user.id
        # booking1 = Booking.objects.all().order_by('-id')
        if int(status) == 1:
            booking1 = Booking.objects.filter((Q(orderStatus=1) | Q(
                orderStatus=2) | Q(orderStatus=3))).order_by('-id')
        elif int(status) == 2:
            booking1 = Booking.objects.filter(
                orderStatus=4).order_by('-id')
        elif int(status) == 3:
            booking1 = Booking.objects.filter(
                orderStatus=9).order_by('-id')
        elif int(status) == 4:
            booking1 = Booking.objects.filter((Q(orderStatus=5) | Q(
                orderStatus=6) | Q(orderStatus=7))).order_by('-id')
        elif int(status) == 5:
            booking1 = Booking.objects.filter(
                orderStatus=8).order_by('-id')

        for eachBooking2 in booking1:
            priductD = Product.objects.filter(
                id=eachBooking2.product_id_id).first()
            # print(priductD.user_id_id)
            # print(".."+str(user_id))
            # print(eachBooking2.orderID)
            if int(priductD.user_id_id) == int(user_id):
                # print(eachBooking2.orderID in booking)
                if (eachBooking2.orderID in booking) == False:
                    booking.append(eachBooking2.orderID)
            # else:
                #         print('..............')
        # print((booking))
        # print(get_unique_numbers(booking))
        # print(set(booking))
        for eachbooking1 in booking:

            if int(status) == 1:
                eachbooking = Booking.objects.filter((Q(orderStatus=1) | Q(
                    orderStatus=2) | Q(orderStatus=3)), orderID=eachbooking1).first()
                productPayablePrice = Booking.objects.filter((Q(orderStatus=1) | Q(
                    orderStatus=2) | Q(orderStatus=3)), orderID=eachbooking.orderID).aggregate(Sum('productPayablePrice'), Sum('productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))
            elif int(status) == 2:
                eachbooking = Booking.objects.filter(
                    orderStatus=4, orderID=eachbooking1).first()
                productPayablePrice = Booking.objects.filter(orderStatus=4, orderID=eachbooking.orderID).aggregate(Sum('productPayablePrice'), Sum(
                    'productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))
            elif int(status) == 3:
                eachbooking = Booking.objects.filter(
                    orderStatus=9, orderID=eachbooking1).first()
                productPayablePrice = Booking.objects.filter(orderStatus=9, orderID=eachbooking.orderID).aggregate(Sum('productPayablePrice'), Sum(
                    'productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))

            elif int(status) == 4:
                eachbooking = Booking.objects.filter((Q(orderStatus=5) | Q(
                    orderStatus=6) | Q(orderStatus=7)), orderID=eachbooking1).first()
                productPayablePrice = Booking.objects.filter((Q(orderStatus=5) | Q(
                    orderStatus=6) | Q(orderStatus=7)), orderID=eachbooking.orderID).aggregate(Sum('productPayablePrice'), Sum('productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))

            elif int(status) == 5:
                eachbooking = Booking.objects.filter(
                    orderStatus=8, orderID=eachbooking1).first()
                productPayablePrice = Booking.objects.filter(orderID=eachbooking.orderID, orderStatus=8).aggregate(Sum('productPayablePrice'), Sum(
                    'productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))

            # eachbooking = Booking.objects.filter(
            #     id=eachbooking1).first()

            # productPayablePrice = Booking.objects.filter(
            #     orderID=eachbooking.orderID).aggregate(Sum('productPayablePrice'), Sum('productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))
            # print(productPayablePrice)
            # print(productPayablePrice['productPayablePrice__sum'])
            bookingDetails = {
                'id': eachbooking.id,
                'OrderID': eachbooking.orderID,
                'orderDate': eachbooking.OrderDate,
                'productPayablePrice': productPayablePrice['productPayablePrice__sum'],
                'productSellingPrice': productPayablePrice['productSellingPrice__sum'],
                'productGST': productPayablePrice['productGST__sum'],
                'deliveryCharge': productPayablePrice['deliveryCharge__sum'],
                'walletAmount': productPayablePrice['walletAmount__sum'],
                'walletPoint': productPayablePrice['walletPoint__sum'],
                'couponDiscount': productPayablePrice['couponDiscount__sum'],
                'couponCode': eachbooking.couponCode,
                'orderStatus': eachbooking.orderStatus,
                'paymentType': eachbooking.paymentType,
                'razorpayPaymentId': eachbooking.razorpayPaymentId,
                'deliveryDate': eachbooking.deliveryDate,
                'returnDate': eachbooking.returnDate,
                'returnExpairStatus': eachbooking.returnExpairStatus,
                'orderInTransitDate': eachbooking.orderInTransitDate,
                'readyForReturnDate': eachbooking.readyForReturnDate,
                'cancelDate': eachbooking.cancelDate,
                'reviewStatus': eachbooking.reviewStatus,
                'booking_id': eachbooking.id,
                'qty': eachbooking.quantity


            }

            # product = Product.objects.filter(id=eachbooking.product_id_id)
            # for eachproduct in product:
            #     productName = eachproduct.productName
            #     Product_id = eachproduct.id
            #     ProductCode = eachproduct.productCode
            #     skuCode = eachproduct.skuCode
            #     mrp = eachproduct.mrp
            #     sellingPrice = eachproduct.sellingPrice
            #     image122 = ProductImage.objects.filter(
            #         productID_id=eachproduct.id)
            #     for eachimage in image122:
            #         image = eachimage.productImage

            #     brand22 = ProductBrand.objects.filter(
            #         id=eachproduct.productBrandID_id)
            #     for eachbrand in brand22:
            #         Brand = eachbrand.brand_name
            #     subcatdel = SubCategory.objects.filter(
            #         id=eachproduct.sub_cat_id_id)
            #     for eachsubcatdel in subcatdel:
            #         gst = eachsubcatdel.gst
            # productDetail = {
            #     'productID': Product_id,
            #     'productName': productName,
            #     'productCode': ProductCode,
            #     'skuCode': skuCode,
            #     'brand': Brand,
            #     'image': str(image),
            #     'mrp': mrp,
            #     'sellingPrice': round(sellingPrice+((sellingPrice*gst)/100))

            # }
            add = ShippingAddress.objects.filter(
                id=eachbooking.shippingAddressId_id)
            for eachadd in add:
                useD = User.objects.filter(id=eachadd.user_id_id).first()
                pincode = eachadd.pincode
                flat = eachadd.flat
                address = eachadd.address
                location = eachadd.location
                landmark = eachadd.landmark
                city = eachadd.city
                district = eachadd.district
                state = eachadd.state
                name = eachadd.name
                phone = eachadd.phone
                optionalPhone = eachadd.optionalPhone
                id = useD.id
                customerID = useD.username
            ShippingAddressDetails = {
                'pincode': pincode,
                'flat': flat,
                'address': address,
                'location': location,
                'landmark': landmark,
                'city': city,
                'district': district,
                'state': state,
                'name': name,
                'phone': phone,
                'id': id,
                'customerID': customerID,
                'optionalPhone': optionalPhone,
            }

            pro = {
                'id': eachbooking.id,
                'bookingDetails': bookingDetails,
                # 'productDetail': productDetail,
                'shippingAddress': ShippingAddressDetails

            }
            booking2.append(pro)
            # print(booking2)
        return Response(booking2)


class vendorsearchBookingAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        user_id = self.request.user.id

        booking2 = []
        ShippingAddressDetails = []
        inputs = request.data
        query_string = inputs['search']
        booking = Booking.objects.filter(
            Q(orderID__icontains=query_string) | Q(
                OrderDate__icontains=query_string)
        ).order_by('-id')
        for eachbooking in booking:
            vendor = Product.objects.filter(id=eachbooking.product_id_id)
            for eachvendor in vendor:
                if eachvendor.user_id_id == user_id:

                    bookingDetails = {
                        'OrderID': eachbooking.orderID,
                        'orderDate': eachbooking.OrderDate,
                        'productPayablePrice': eachbooking.productPayablePrice,
                        'productSellingPrice': eachbooking.productSellingPrice,
                        'productGST': eachbooking.productGST,
                        'deliveryCharge': eachbooking.deliveryCharge,
                        'walletAmount': eachbooking.walletAmount,
                        'couponDiscount': eachbooking.couponDiscount	,
                        'couponCode': eachbooking.couponCode,
                        'orderStatus': eachbooking.orderStatus,
                        'paymentType': eachbooking.paymentType,
                        'razorpayPaymentId': eachbooking.razorpayPaymentId,
                        'deliveryDate': eachbooking.deliveryDate,
                        'returnDate': eachbooking.returnDate,
                        'returnExpairStatus': eachbooking.returnExpairStatus,
                        'redeemStatus': eachbooking.redeemStatus,
                        'orderInTransitDate': eachbooking.orderInTransitDate,
                        'readyForReturnDate': eachbooking.readyForReturnDate,
                        'cancelDate': eachbooking.cancelDate,
                        'reviewStatus': eachbooking.reviewStatus,
                        'booking_id': eachbooking.id,
                        'qty': eachbooking.quantity

                    }

                    product = Product.objects.filter(
                        id=eachbooking.product_id_id)
                    for eachproduct in product:
                        productName = eachproduct.productName
                        Product_id = eachproduct.id
                        ProductCode = eachproduct.productCode
                        mrp = eachproduct.mrp
                        sellingPrice = eachproduct.sellingPrice
                        withoutGstPrice = eachproduct.wihoutgstprice
                        image122 = ProductImage.objects.filter(
                            productID_id=eachproduct.id)
                        for eachimage in image122:
                            image = eachimage.productImage

                        brand22 = ProductBrand.objects.filter(
                            id=eachproduct.productBrandID_id)
                        for eachbrand in brand22:
                            Brand = eachbrand.brand_name
                        subcatdel = SubCategory.objects.filter(
                            id=eachproduct.sub_cat_id_id)
                        for eachsubcatdel in subcatdel:
                            gst = eachsubcatdel.gst
                            comm = eachsubcatdel.commission
                    productDetail = {
                        'productID': Product_id,
                        'productName': productName,
                        'productCode': ProductCode,
                        'brand': Brand,
                        'image': str(image),
                        'mrp': mrp,
                        'sellingPrice': round(sellingPrice),
                        'comm': round((withoutGstPrice*comm)/100)
                    }
                    add = ShippingAddress.objects.filter(
                        id=eachbooking.shippingAddressId_id)
                    for eachadd in add:
                        pincode = eachadd.pincode
                        flat = eachadd.flat
                        address = eachadd.address
                        location = eachadd.location
                        landmark = eachadd.landmark
                        city = eachadd.city
                        district = eachadd.district
                        state = eachadd.state
                        name = eachadd.name
                        phone = eachadd.phone
                        optionalPhone = eachadd.optionalPhone
                    ShippingAddressDetails = {
                        'pincode': pincode,
                        'flat': flat,
                        'address': address,
                        'location': location,
                        'landmark': landmark,
                        'city': city,
                        'district': district,
                        'state': state,
                        'name': name,
                        'phone': phone,
                        'optionalPhone': optionalPhone,
                    }

                    pro = {
                        'bookingDetails': bookingDetails,
                        'productDetail': productDetail,
                        'shippingAddress': ShippingAddressDetails,

                    }
                    booking2.append(pro)

        return Response(booking2)


class userReturnBookingAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        newrel = []
        user_id = self.request.user.id
        user_details = User.objects.filter(id=user_id).first()
        phone_no = self.request.user.phone
        email = self.request.user.email
        name = self.request.user.name
        inputs = request.data
        bookingUpdate = Booking.objects.filter(
            id=inputs['booking_id']).update(orderStatus=5)
        reasonCreate = Reason.objects.create(
            user_id_id=user_id, booking_id_id=inputs['booking_id'], type='Return', reason=inputs['return_option'], message=inputs['return_msg'])
        newrel = {
            'status': 'Return Request Send Successfully',
            'code': 1,
        }
        sms_body = 'Return Request : We have receive a return request of your order. We will notify you as soon as possible.'
        # response = requests.get(
        #     "http://weberleads.in/http-tokenkeyapi.php?authentic-key=3134696e7374616e745f6765747761793631321586003895&senderid=INGWAY&route=2&number="+phone_no+"&message="+sms_body)
        # data = {'title': 'Return Request', 'content': sms_body, 'email_subject': 'Return Request',
        #         'to_email': user_details.email, 'from_email': settings.EMAIL_HOST_USERS}
        # Util.email_send(data)
        # message ='Booking Canceled : Hi, your order has been canceled as per your request.'
        template_id = ''
        # smsSend(phone_no, sms_body, template_id)
        # data = {
        #     'name': name,
        #     'email': email,
        #     'subject': 'Return Request Successfully',
        #     'message': ' We have receive a return request of your order. We will notify you as soon as possible.',
        #     'from_email': settings.EMAIL_HOST_USER
        # }
        # Util.email_send(data)
        return Response(newrel)


class userSingleBookingAPIView(views.APIView):
    def get(self, request, id):
        b_id = id
        booking2 = []
        ShippingAddressDetails = []
        booking = Booking.objects.filter(id=b_id).order_by('-id')
        for eachbooking in booking:

            bookingDetails = {
                'OrderID': eachbooking.orderID,
                'orderDate': eachbooking.OrderDate,
                'productPayablePrice': eachbooking.productPayablePrice,
                'productSellingPrice': eachbooking.productSellingPrice,
                'productGST': eachbooking.productGST,
                'deliveryCharge': eachbooking.deliveryCharge,
                'walletAmount': eachbooking.walletAmount,
                'walletPoint': eachbooking.walletPoint,
                'couponDiscount': eachbooking.couponDiscount	,
                'couponCode': eachbooking.couponCode,
                'orderStatus': eachbooking.orderStatus,
                'paymentType': eachbooking.paymentType,
                'razorpayPaymentId': eachbooking.razorpayPaymentId,
                'deliveryDate': eachbooking.deliveryDate,
                'returnDate': eachbooking.returnDate,
                'orderInTransitDate': eachbooking.orderInTransitDate,
                'readyForReturnDate': eachbooking.readyForReturnDate,
                'cancelDate': eachbooking.cancelDate,
                'reviewStatus': eachbooking.reviewStatus,
                'booking_id': eachbooking.id,
                'qty': eachbooking.quantity,
                'deliveryBoyId': eachbooking.deliveryBoyId,
                'returnBoyId': eachbooking.returnBoyId

            }

            product = Product.objects.filter(id=eachbooking.product_id_id)
            for eachproduct in product:
                productName = eachproduct.productName
                Product_id = eachproduct.id
                ProductCode = eachproduct.productCode
                mrp = eachproduct.mrp
                sellingPrice = eachproduct.sellingPrice
                size = eachproduct.size
                color = eachproduct.color
                vendorId = eachproduct.user_id_id
                skuCode = eachproduct.skuCode
                image122 = ProductImage.objects.filter(
                    productID_id=eachproduct.id)
                for eachimage in image122:
                    image = eachimage.productImage

                brand22 = ProductBrand.objects.filter(
                    id=eachproduct.productBrandID_id)
                for eachbrand in brand22:
                    Brand = eachbrand.brand_name
                subcatdel = SubCategory.objects.filter(
                    id=eachproduct.sub_cat_id_id)
                for eachsubcatdel in subcatdel:
                    gst = eachsubcatdel.gst
            productDetail = {
                'productID': Product_id,
                'productName': productName,
                'productCode': ProductCode,
                'skuCode': skuCode,
                'brand': Brand,
                'image': str(image),
                'mrp': mrp,
                'size': size,
                'color': color,
                'sellingPrice': round(sellingPrice+((sellingPrice*gst)/100))

            }
            add = ShippingAddress.objects.filter(
                id=eachbooking.shippingAddressId_id)
            for eachadd in add:
                pincode = eachadd.pincode
                flat = eachadd.flat
                address = eachadd.address
                location = eachadd.location
                landmark = eachadd.landmark
                city = eachadd.city
                district = eachadd.district
                state = eachadd.state
                name = eachadd.name
                phone = eachadd.phone
                optionalPhone = eachadd.optionalPhone
            ShippingAddressDetails = {
                'pincode': pincode,
                'flat': flat,
                'address': address,
                'location': location,
                'landmark': landmark,
                'city': city,
                'district': district,
                'state': state,
                'name': name,
                'phone': phone,
                'optionalPhone': optionalPhone,
            }

            add1 = ShippingAddress.objects.filter(user_id_id=vendorId)[:1]
            for eachadd1 in add1:
                pincode = eachadd1.pincode
                flat = eachadd1.flat
                address = eachadd1.address
                location = eachadd1.location
                landmark = eachadd1.landmark
                city = eachadd1.city
                district = eachadd1.district
                state = eachadd1.state
                name = eachadd1.name
                phone = eachadd1.phone
                optionalPhone = eachadd1.optionalPhone
            ReturnAddressDetails = {
                'pincode': pincode,
                'flat': flat,
                'address': address,
                'location': location,
                'landmark': landmark,
                'city': city,
                'district': district,
                'state': state,
                'name': name,
                'phone': phone,
                'optionalPhone': optionalPhone,
            }

            vendor = VendorDetails.objects.filter(user_id_id=vendorId)
            for vendorDe in vendor:
                companyName = vendorDe.companyName,
                gst = vendorDe.gstNumber,
                vendorSign = str(vendorDe.vendorSign),
                companyLogo = str(vendorDe.companyLogo),

            vendorDetails = {
                'companyName': companyName,
                'gst': gst,
                'vendorSign': vendorSign,
                'companyLogo': companyLogo

            }
           
            if eachbooking.deliveryBoyName:
                DeliveryboyDetails = {
                    'name': eachbooking.deliveryBoyName,
                    'phone': eachbooking.deliveryBoyPhone,
                }
            else:
                DeliveryboyDetails = {}
            if eachbooking.returnBoyName:
                ReturnboyDetails = {
                    'name': eachbooking.returnBoyName,
                    'phone': eachbooking.returnBoyPhone,
                }
            else:
                ReturnboyDetails = {}
           
            billaddress = BillingAddress.objects.filter(
                user_id_id=eachbooking.user_id_id)
            for eachbill in billaddress:
                pincode = eachbill.pincode
                flat = eachbill.flat
                address = eachbill.address
                location = eachbill.location
                city = eachbill.city
                district = eachbill.district
                state = eachbill.state
            BillingAddressDetails = {
                'pincode': pincode,
                'flat': flat,
                'address': address,
                'location': location,
                'city': city,
                'district': district,
                'state': state,
            }
            users = User.objects.filter(id=eachbooking.user_id_id)

            for user in users:
                uname = user.name
                uphone = user.phone
                uemail = user.email
                ucID = user.username
            UserDetails = {
                'name': uname,
                'phone': uphone,
                'email': uemail,
                'customerID': ucID,
            }

            pro = {
                'bookingDetails': bookingDetails,
                'productDetail': productDetail,
                'shippingAddress': ShippingAddressDetails,
                'deliveryBoy': DeliveryboyDetails,
                'returnBoy': ReturnboyDetails,
                'billingAddress': BillingAddressDetails,
                'userDetails': UserDetails,
                'ReturnAddress': ReturnAddressDetails,
                'vendorDetails': vendorDetails
            }
            booking2.append(pro)

        return Response(booking2)


class vendorWiseBookingDetails(views.APIView):
    def get(self, request, id, status):
        productSellingPrice = 0
        couponDiscount = 0
        walletAmount = 0
        walletPoint = 0
        deliveryCharge = 0
        orderStatus = 0
        booking = []
        if int(status) == 1:
            booking = Booking.objects.filter((Q(orderStatus=1) | Q(orderStatus=2) | Q(orderStatus=3)),
                                             orderID=id).order_by('-id')
            bookingAddress = Booking.objects.filter(
                (Q(orderStatus=1) | Q(orderStatus=2) | Q(orderStatus=3)), orderID=id).first()
        elif int(status) == 2:
            booking = Booking.objects.filter(
                orderStatus=4, orderID=id).order_by('-id')
            bookingAddress = Booking.objects.filter(
                orderStatus=4, orderID=id).first()
        elif int(status) == 3:
            booking = Booking.objects.filter(
                orderStatus=9, orderID=id).order_by('-id')
            bookingAddress = Booking.objects.filter(
                orderStatus=9, orderID=id).first()
        elif int(status) == 4:
            booking = Booking.objects.filter((Q(orderStatus=5) | Q(
                orderStatus=6) | Q(orderStatus=7)), orderID=id).order_by('-id')
            bookingAddress = Booking.objects.filter((Q(orderStatus=5) | Q(
                orderStatus=6) | Q(orderStatus=7)), orderID=id).first()
        elif int(status) == 5:
            booking = Booking.objects.filter(
                orderStatus=8, orderID=id).order_by('-id')
            bookingAddress = Booking.objects.filter(
                orderID=id, orderStatus=8).first()
        elif int(status) == 0:
            booking = Booking.objects.filter( id=id).order_by('-id')
            bookingAddress = Booking.objects.filter(id=id).first()
            # print(status)
            # print(booking)
        # booking = Booking.objects.filter(
        #     orderID=id).order_by('-id')
        productArray = []
        if booking:
            # print(booking)
            for eachBooking in booking:
                eachproduct = Product.objects.filter(
                    id=eachBooking.product_id_id).first()
                productName = eachproduct.productName
                Product_id = eachproduct.id
                ProductCode = eachproduct.productCode
                mrp = eachproduct.mrp
                sellingPrice = eachproduct.sellingPrice
                size = eachproduct.size
                color = eachproduct.color
                vendorId = eachproduct.user_id_id
                skuCode = eachproduct.skuCode
                subcatdel = SubCategory.objects.filter(
                    id=eachproduct.sub_cat_id_id)
                for eachsubcatdel in subcatdel:
                    gst = eachsubcatdel.gst
                    com = eachsubcatdel.commission
                cancelReason = Reason.objects.filter(
                    booking_id_id=eachBooking.id, type="Cancel").first()
                if cancelReason:
                    reasonArr = {
                        'reason': cancelReason.reason,
                        'msg': cancelReason.message
                    }
                else:
                    reasonArr = {
                        'reason': '',
                        'msg': ''
                    }
                returnReason = Reason.objects.filter(
                    booking_id_id=eachBooking.id, type="Return").first()
                if returnReason:
                    reasonArr2 = {
                        'reason': returnReason.reason,
                        'msg': returnReason.message
                    }
                else:
                    reasonArr2 = {
                        'reason': '',
                        'msg': ''
                    }

                new = {
                    'productPayablePrice': eachBooking.productPayablePrice,
                    'productSellingPrice': eachBooking.productSellingPrice,
                    'productGST': eachBooking.productGST,
                    'orderStatus': eachBooking.orderStatus,
                    'deliveryDate': eachBooking.deliveryDate,
                    'returnDate': eachBooking.returnDate,
                    'orderInTransitDate': eachBooking.orderInTransitDate,
                    'readyForReturnDate': eachBooking.readyForReturnDate,
                    'cancelDate': eachBooking.cancelDate,
                    'booking_id': eachBooking.id,
                    'qty': eachBooking.quantity,
                    'productID': Product_id,
                    'productName': productName,
                    'productCode': ProductCode,
                    'skuCode': skuCode,
                    'mrp': mrp,
                    'size': size,
                    'color': color,
                    'sellingPrice': round(sellingPrice),
                    'cancelReason': reasonArr,
                    'returnReason': reasonArr2,
                    'admin_com': round((sellingPrice*com)/100),
                    'vendor_id': vendorId
                }
                productSellingPrice = round(eachBooking.productSellingPrice * eachBooking.quantity)
                couponDiscount = couponDiscount+eachBooking.couponDiscount
                walletAmount = walletAmount+eachBooking.walletAmount
                walletPoint = walletPoint+eachBooking.walletPoint
                deliveryCharge = deliveryCharge+eachBooking.deliveryCharge
                # print(eachBooking.orderStatus)
                # if int(status) == 4:
                #     if eachBooking.orderStatus == 5 or eachBooking.orderStatus == 6 or eachBooking.orderStatus == 7 or eachBooking.orderStatus == 8:
                #         orderStatus = eachBooking.orderStatus
                # elif int(status) == 5:
                #     if eachBooking.orderStatus == 5 or eachBooking.orderStatus == 6 or eachBooking.orderStatus == 7 or eachBooking.orderStatus == 8:
                orderStatus = eachBooking.orderStatus

                productArray.append(new)

            eachadd = ShippingAddress.objects.filter(
                id=bookingAddress.shippingAddressId_id).first()
            pincode = eachadd.pincode
            flat = eachadd.flat
            address = eachadd.address
            location = eachadd.location
            landmark = eachadd.landmark
            city = eachadd.city
            district = eachadd.district
            state = eachadd.state
            name = eachadd.name
            phone = eachadd.phone
            optionalPhone = eachadd.optionalPhone
            ShippingAddressDetails = {
                'pincode': pincode,
                'flat': flat,
                'address': address,
                'location': location,
                'landmark': landmark,
                'city': city,
                'district': district,
                'state': state,
                'name': name,
                'phone': phone,
                'optionalPhone': optionalPhone,
            }
            eachbill = BillingAddress.objects.filter(
                user_id_id=bookingAddress.user_id_id).first()
            pincode = eachbill.pincode
            flat = eachbill.flat
            address = eachbill.address
            location = eachbill.location
            city = eachbill.city
            district = eachbill.district
            state = eachbill.state
            BillingAddressDetails = {
                'pincode': pincode,
                'flat': flat,
                'address': address,
                'location': location,
                'city': city,
                'district': district,
                'state': state,
            }
            users = User.objects.filter(id=bookingAddress.user_id_id).first()
            uname = users.name
            uphone = users.phone
            uemail = users.email
            ucID = users.username
            UserDetails = {
                'name': uname,
                'phone': uphone,
                'email': uemail,
                'customerID': ucID,
            }
            bookingArr = {
                'orderID': id,
                'orderDate': bookingAddress.OrderDate,
                'productSellingPrice': (productSellingPrice),
                'couponDiscount': couponDiscount,
                'walletAmount': walletAmount,
                'walletPoint': walletPoint,
                'deliveryCharge': deliveryCharge,
                'paymentType': bookingAddress.paymentType,
                'razorpayPaymentId': bookingAddress.razorpayPaymentId,
                'couponCode': bookingAddress.couponCode,
                'orderStatus': orderStatus,
                'deliveryBoyName': bookingAddress.deliveryBoyName,
                'deliveryBoyPhone': bookingAddress.deliveryBoyPhone,
                'deliveryDate': bookingAddress.deliveryDate,
                'returnBoyName': bookingAddress.returnBoyName,
                'returnBoyPhone': bookingAddress.returnBoyPhone,
                'returnDate': bookingAddress.returnDate,
                'invoiceNumber': bookingAddress.invoiceNumber,
                'invoiceDate': bookingAddress.invoiceDate,

            }
            returnArray = {
                'bookingArray': bookingArr,
                'shippingAddress': ShippingAddressDetails,
                'billingAddress': BillingAddressDetails,
                'userDetails': UserDetails,
                'productArray': productArray
            }
        else:
            returnArray = {
                'bookingArray': [],
                'shippingAddress': [],
                'billingAddress': [],
                'userDetails': [],
                'productArray': []
            }
        return Response(returnArray)


class InvoiceBookingDetails(views.APIView):
    def get(self, request, id):
        productSellingPrice = 0
        couponDiscount = 0
        walletAmount = 0
        walletPoint = 0
        deliveryCharge = 0
        orderStatus = 0
        totalQty = 0
        booking = []
        booking = Booking.objects.filter(Q(orderStatus=2) | Q(orderStatus=3) | Q(orderStatus=4) | Q(orderStatus=5) | Q(orderStatus=6) | Q(orderStatus=7) | Q(orderStatus=8),
                                         invoiceNumber=id).order_by('-id')
        # print(status)
        # print(booking)
        productArray = []
        if booking:
            # print(booking)
            for eachBooking in booking:
                eachproduct = Product.objects.filter(
                    id=eachBooking.product_id_id).first()
                productName = eachproduct.productName
                Product_id = eachproduct.id
                ProductCode = eachproduct.productCode
                mrp = eachproduct.mrp
                sellingPrice = eachproduct.sellingPrice
                size = eachproduct.size
                color = eachproduct.color
                vendorId = eachproduct.user_id_id
                skuCode = eachproduct.skuCode
                subcatdel = SubCategory.objects.filter(
                    id=eachproduct.sub_cat_id_id)
                for eachsubcatdel in subcatdel:
                    gst = eachsubcatdel.gst
                new = {
                    'productPayablePrice': eachBooking.productPayablePrice,
                    'productSellingPrice': eachBooking.productSellingPrice,
                    'productGST': eachBooking.productGST,
                    'orderStatus': eachBooking.orderStatus,
                    'deliveryDate': eachBooking.deliveryDate,
                    'returnDate': eachBooking.returnDate,
                    'orderInTransitDate': eachBooking.orderInTransitDate,
                    'readyForReturnDate': eachBooking.readyForReturnDate,
                    'cancelDate': eachBooking.cancelDate,
                    'booking_id': eachBooking.id,
                    'qty': eachBooking.quantity,
                    'productID': Product_id,
                    'productName': productName,
                    'productCode': ProductCode,
                    'skuCode': skuCode,
                    'mrp': mrp,
                    'size': size,
                    'color': color,
                    'sellingPrice': round(sellingPrice)
                }
                productSellingPrice = round(eachBooking.productSellingPrice*eachBooking.quantity)
                couponDiscount = couponDiscount+eachBooking.couponDiscount
                walletAmount = walletAmount+eachBooking.walletAmount
                walletPoint = walletPoint+eachBooking.walletPoint
                deliveryCharge = deliveryCharge+eachBooking.deliveryCharge
                orderStatus = eachBooking.orderStatus
                totalQty = totalQty+eachBooking.quantity
                productArray.append(new)
            bookingAddress = Booking.objects.filter(invoiceNumber=id).first()
            eachadd = ShippingAddress.objects.filter(
                id=bookingAddress.shippingAddressId_id).first()
            pincode = eachadd.pincode
            flat = eachadd.flat
            address = eachadd.address
            location = eachadd.location
            landmark = eachadd.landmark
            city = eachadd.city
            district = eachadd.district
            state = eachadd.state
            name = eachadd.name
            phone = eachadd.phone
            optionalPhone = eachadd.optionalPhone
            ShippingAddressDetails = {
                'pincode': pincode,
                'flat': flat,
                'address': address,
                'location': location,
                'landmark': landmark,
                'city': city,
                'district': district,
                'state': state,
                'name': name,
                'phone': phone,
                'optionalPhone': optionalPhone,
            }
            print(vendorId)
            users = User.objects.filter(id=bookingAddress.user_id_id).first()
            uname = users.name
            uphone = users.phone
            uemail = users.email
            ucID = users.username
            UserDetails = {
                'name': uname,
                'phone': uphone,
                'email': uemail,
                'customerID': ucID,
            }
            vendor = VendorDetails.objects.filter(user_id_id=vendorId).first()
            companyName = vendor.companyName,
            gst = vendor.gstNumber,
            vendorSign = str(vendor.vendorSign),
            companyLogo = str(vendor.companyLogo),
            bookingArr = {
                'orderID': bookingAddress.orderID,
                'orderDate': bookingAddress.OrderDate,
                'productSellingPrice': math.ceil(productSellingPrice),
                'couponDiscount': couponDiscount,
                'walletAmount': walletAmount,
                'walletPoint': walletPoint,
                'deliveryCharge': deliveryCharge,
                'paymentType': bookingAddress.paymentType,
                'razorpayPaymentId': bookingAddress.razorpayPaymentId,
                'couponCode': bookingAddress.couponCode,
                'orderStatus': orderStatus,
                'deliveryBoyName': bookingAddress.deliveryBoyName,
                'deliveryBoyPhone': bookingAddress.deliveryBoyPhone,
                'deliveryDate': bookingAddress.deliveryDate,
                'returnBoyName': bookingAddress.returnBoyName,
                'returnBoyPhone': bookingAddress.returnBoyPhone,
                'returnDate': bookingAddress.returnDate,
                'invoiceNumber': bookingAddress.invoiceNumber,
                'invoiceDate': bookingAddress.invoiceDate,
                'totalQty': totalQty,
                'vendorCompanyName': companyName,
                'vebdorGst': gst,
                'vendorSign': vendorSign,
                'vendorCompanyLogo': companyLogo


            }
            returnArray = {
                'bookingArray': bookingArr,
                'shippingAddress': ShippingAddressDetails,
                'returnAddress': ShippingAddressDetails,
                'billingAddress': ShippingAddressDetails,
                'userDetails': UserDetails,
                'productArray': productArray
            }
        else:
            returnArray = {
                'bookingArray': [],
                'shippingAddress': [],
                'returnAddress': [],
                'billingAddress': [],
                'userDetails': [],
                'productArray': []
            }
        return Response(returnArray)


class statusChange(views.APIView):
    def post(self, request, orderID):
        inputs = request.data
        status = inputs['status']
        productPayablePrice = 0
        couponDiscount = 0
        user_id = 0
        walletPoint = 0
        bookingArr = Booking.objects.filter(
            orderID=orderID, orderStatus=status)
        if bookingArr:
            for eachBooking in bookingArr:
                print((eachBooking.user_id_id))
                if int(status) == 1:
                    Booking.objects.filter(id=eachBooking.id).update(
                        orderStatus=status+1,
                        orderInTransitDate=date.today()
                    )
                    user_id = eachBooking.user_id_id
                elif int(status) == 2:
                    Booking.objects.filter(id=eachBooking.id).update(
                        orderStatus=status+1,
                        deliveryBoyName=inputs['name'],
                        deliveryBoyPhone=inputs['phone'],
                        outForDeliveryDate=date.today()

                    )
                    user_id = eachBooking.user_id_id
                elif int(status) == 3:
                    Booking.objects.filter(id=eachBooking.id).update(
                        orderStatus=status+1,
                        deliveryDate=date.today()
                    )
                    user_id = eachBooking.user_id_id
                elif int(status) == 5:
                    Booking.objects.filter(id=eachBooking.id).update(
                        orderStatus=status+1,
                        readyForReturnDate=date.today()
                    )
                    user_id = eachBooking.user_id_id
                elif int(status) == 6:
                    Booking.objects.filter(id=eachBooking.id).update(
                        orderStatus=status+1,
                        returnBoyName=inputs['name'],
                        returnBoyPhone=inputs['phone'],
                        outForPicupDate=date.today()
                    )
                    user_id = eachBooking.user_id_id
                elif int(status) == 7:
                    Booking.objects.filter(id=eachBooking.id).update(
                        orderStatus=status+1,
                        returnDate=date.today()
                    )
                    eachbooking1 = Booking.objects.filter(
                        id=eachBooking.id).first()
                    productPayablePrice = productPayablePrice+eachbooking1.productPayablePrice
                    couponDiscount = couponDiscount+eachbooking1.couponDiscount
                    walletPoint = walletPoint+eachbooking1.walletPoint
                    user_id = eachbooking1.user_id_id

                else:
                    Booking.objects.filter(id=eachBooking.id).update(
                        orderStatus=status+1
                    )
                    user_id = eachBooking.user_id_id

            if int(status) == 7:
                wallet = Wallet.objects.filter(
                    user_id_id=user_id).first()
                currentWalletBalance = wallet.amount

                RefundableAmount = productPayablePrice-couponDiscount
                updatedWalletBalance = currentWalletBalance+RefundableAmount
                walletUpdate = Wallet.objects.filter(
                    user_id_id=user_id).update(amount=updatedWalletBalance)
                WalletTransCreate = WalletTransaction.objects.create(
                    user_id_id=user_id, transactionAmount=RefundableAmount, afterTransactionAmount=updatedWalletBalance, remarks='Return Order', transactionType='CREDIT')
            # sms
            userDetails = User.objects.filter(id=user_id).first()
            phoneNumber = userDetails.phone
            email = userDetails.email
            name = userDetails.name
            if int(status) == 1:
                sms = "Order in Transit : Your order is dispatched via our courier partner. "
                message="Your order is dispatched via our courier partner. "
                subject = 'Out for Transit'
                template_id = ''
            elif int(status) == 2:
                sms = "Out for Delivery : Hi " + str(userDetails.name) + ", Your order will bo delivered today. Our delivery boy Mr." + str(
                    inputs['name']) + ", Contact number " + inputs['phone'] + " will deliver your order."
                subject = 'Out for Delivery'
                template_id = ''
                message="Hi " + str(userDetails.name) + ", Your order will bo delivered today. Our delivery boy Mr." + str(
                    inputs['name']) + ", Contact number " + inputs['phone'] + " will deliver your order."
            elif int(status) == 3:
                sms = "Delivered : Thank you for ordering with Crowd, we are delighted to inform you that your order has been successfully delivered. Please check name quantity and expiry of your items and in case of any issue or item missing or wrong item please contact to us."
                subject = 'Order Delivered'
                template_id = ''
                message="Thank you for ordering with Crowd, we are delighted to inform you that your order has been successfully delivered. Please check name quantity and expiry of your items and in case of any issue or item missing or wrong item please contact to us."
            # elif int(status)==4 :
            #     sms = "Delivered : Thank you for ordering with Crowd, we are delighted to inform you that your order has been successfully delivered. Please check name quantity and expiry of your items and in case of any issue or item missing or wrong item please contact to us."
            #     subject = 'Order Delivered'
            #     template_id=''

            elif int(status) == 6:
                sms = "Out for Pickup : Hi " + str(userDetails.name) + ",  Your return items pickup today. Our delivery boy Mr." + str(
                    inputs['name']) + ", Contact number " + inputs['phone'] + " will receive your order."
                subject = 'Out for Pickup '
                message = "Your return items pickup today. Our delivery boy Mr." + \
                    str(inputs['name']) + ", Contact number " + \
                    inputs['phone'] + " will receive your order."
                template_id = ''

            elif int(status) == 7:
                sms = "Returned : Your return items received to admin. Return request is successfully completed and the booking amount is refunded to your Wallet."
                subject = 'Order Returned'
                message = "Your return items received to admin. Return request is successfully completed and the booking amount is refunded to your Wallet."
                template_id = ''
            # try:
            #     smsSend(phoneNumber, sms, template_id)
            #     data = {
            #         'name': name,
            #         'email': email,
            #         'subject': subject,
            #         'message': message,
            #         'from_email': settings.EMAIL_HOST_USER
            #     }
            #     Util.email_send(data)
            # except:
            #     print("An exception occurred")           
            returnArr = {
                'status': 'Status Change Successfully'
            }
        else:
            returnArr = {
                'status': 'No Booking Found'
            }
        return Response(returnArr)


class invoiceGenerate(views.APIView):
    def post(self, request, orderID):
        inputs = request.data
        status = inputs['status']
        bookingArr = Booking.objects.filter(
            orderID=orderID, orderStatus=status)
        if bookingArr:
            su = shortuuid.ShortUUID().random(length=10)
            for eachBooking in bookingArr:
                Booking.objects.filter(id=eachBooking.id).update(
                    invoiceNumber=su.upper(),
                    invoiceDate=date.today()
                )

                returnArr = {
                    'status': 'Invoice Generate Successfully'
                }
        else:
            returnArr = {
                'status': 'No Booking Found'
            }
        return Response(returnArr)


class salesReportAPIView(views.APIView):
    def post(self, request):
        inputs = request.data
        booking2 = []
        booking = Booking.objects.filter(OrderDate__range=(
            inputs['start_date'], inputs['end_date'])).order_by('-id')
        for eachbooking in booking:

            bookingDetails = {
                'OrderID': eachbooking.orderID,
                'orderDate': eachbooking.OrderDate,
                'productPayablePrice': eachbooking.productPayablePrice,
            }
            users = User.objects.filter(id=eachbooking.user_id_id)

            for user in users:
                uname = user.name
                uphone = user.phone
                uemail = user.email
            UserDetails = {
                'name': uname,
                'phone': uphone,
                'email': uemail
            }

            pro = {
                'bookingDetails': bookingDetails,
                'userDetails': UserDetails
            }
            booking2.append(pro)
        return Response(booking2)


class taxsReportAPIView(views.APIView):
    def post(self, request):
        inputs = request.data
        booking2 = []
        booking = Booking.objects.filter(OrderDate__range=(
            inputs['start_date'], inputs['end_date'])).order_by('-id')
        for eachbooking in booking:

            bookingDetails = {
                'OrderID': eachbooking.orderID,
                'orderDate': eachbooking.OrderDate,
                'productPayablePrice': eachbooking.productPayablePrice,
                'productGST': eachbooking.productGST,
                'productSellingPrice': eachbooking.productSellingPrice,
                'quantity': eachbooking.quantity
            }
            pro = {
                'bookingDetails': bookingDetails,
            }
            booking2.append(pro)
        return Response(booking2)


class adminBookingAPIView(views.APIView):
    def get(self, request, status):
        booking2 = []
        booking = []
        ShippingAddressDetails = []

        # booking1 = Booking.objects.all().order_by('-id')
        if int(status) == 1:
            booking1 = Booking.objects.filter((Q(orderStatus=1) | Q(
                orderStatus=2) | Q(orderStatus=3))).order_by('-id')
        elif int(status) == 2:
            booking1 = Booking.objects.filter(
                orderStatus=4).order_by('-id')
        elif int(status) == 3:
            booking1 = Booking.objects.filter(
                orderStatus=9).order_by('-id')
        elif int(status) == 4:
            booking1 = Booking.objects.filter((Q(orderStatus=5) | Q(
                orderStatus=6) | Q(orderStatus=7))).order_by('-id')
        elif int(status) == 5:
            booking1 = Booking.objects.filter(
                orderStatus=8).order_by('-id')

        for eachBooking2 in booking1:
            if (eachBooking2.orderID in booking) == False:
                booking.append(eachBooking2.orderID)

        for eachbooking1 in booking:
            if int(status) == 1:
                eachbooking = Booking.objects.filter((Q(orderStatus=1) | Q(
                    orderStatus=2) | Q(orderStatus=3)), orderID=eachbooking1).first()
                productPayablePrice = Booking.objects.filter((Q(orderStatus=1) | Q(
                    orderStatus=2) | Q(orderStatus=3)), orderID=eachbooking.orderID).aggregate(Sum('productPayablePrice'), Sum('productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))
            elif int(status) == 2:
                eachbooking = Booking.objects.filter(
                    orderStatus=4, orderID=eachbooking1).first()
                productPayablePrice = Booking.objects.filter(orderStatus=4, orderID=eachbooking.orderID).aggregate(Sum('productPayablePrice'), Sum(
                    'productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))
            elif int(status) == 3:
                eachbooking = Booking.objects.filter(
                    orderStatus=9, orderID=eachbooking1).first()
                productPayablePrice = Booking.objects.filter(orderStatus=9, orderID=eachbooking.orderID).aggregate(Sum('productPayablePrice'), Sum(
                    'productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))

            elif int(status) == 4:
                eachbooking = Booking.objects.filter((Q(orderStatus=5) | Q(
                    orderStatus=6) | Q(orderStatus=7)), orderID=eachbooking1).first()
                productPayablePrice = Booking.objects.filter((Q(orderStatus=5) | Q(
                    orderStatus=6) | Q(orderStatus=7)), orderID=eachbooking.orderID).aggregate(Sum('productPayablePrice'), Sum('productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))

            elif int(status) == 5:
                eachbooking = Booking.objects.filter(
                    orderStatus=8, orderID=eachbooking1).first()
                productPayablePrice = Booking.objects.filter(orderID=eachbooking.orderID, orderStatus=8).aggregate(Sum('productPayablePrice'), Sum(
                    'productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))

            # eachbooking = Booking.objects.filter(
            #     id=eachbooking1).first()

            # productPayablePrice = Booking.objects.filter(
            #     orderID=eachbooking.orderID).aggregate(Sum('productPayablePrice'), Sum('productSellingPrice'), Sum('productGST'), Sum('deliveryCharge'), Sum('walletAmount'), Sum('walletPoint'), Sum('couponDiscount'))
            # print(productPayablePrice)
            # print(productPayablePrice['productPayablePrice__sum'])
            bookingDetails = {
                'id': eachbooking.id,
                'OrderID': eachbooking.orderID,
                'orderDate': eachbooking.OrderDate,
                'productPayablePrice': productPayablePrice['productPayablePrice__sum'],
                'productSellingPrice': productPayablePrice['productSellingPrice__sum'],
                'productGST': productPayablePrice['productGST__sum'],
                'deliveryCharge': productPayablePrice['deliveryCharge__sum'],
                'walletAmount': productPayablePrice['walletAmount__sum'],
                'walletPoint': productPayablePrice['walletPoint__sum'],
                'couponDiscount': productPayablePrice['couponDiscount__sum'],
                'couponCode': eachbooking.couponCode,
                'orderStatus': eachbooking.orderStatus,
                'paymentType': eachbooking.paymentType,
                'razorpayPaymentId': eachbooking.razorpayPaymentId,
                'deliveryDate': eachbooking.deliveryDate,
                'returnDate': eachbooking.returnDate,
                'returnExpairStatus': eachbooking.returnExpairStatus,
                'orderInTransitDate': eachbooking.orderInTransitDate,
                'readyForReturnDate': eachbooking.readyForReturnDate,
                'cancelDate': eachbooking.cancelDate,
                'reviewStatus': eachbooking.reviewStatus,
                'booking_id': eachbooking.id,
                'qty': eachbooking.quantity


            }

            # product = Product.objects.filter(id=eachbooking.product_id_id)
            # for eachproduct in product:
            #     productName = eachproduct.productName
            #     Product_id = eachproduct.id
            #     ProductCode = eachproduct.productCode
            #     skuCode = eachproduct.skuCode
            #     mrp = eachproduct.mrp
            #     sellingPrice = eachproduct.sellingPrice
            #     image122 = ProductImage.objects.filter(
            #         productID_id=eachproduct.id)
            #     for eachimage in image122:
            #         image = eachimage.productImage

            #     brand22 = ProductBrand.objects.filter(
            #         id=eachproduct.productBrandID_id)
            #     for eachbrand in brand22:
            #         Brand = eachbrand.brand_name
            #     subcatdel = SubCategory.objects.filter(
            #         id=eachproduct.sub_cat_id_id)
            #     for eachsubcatdel in subcatdel:
            #         gst = eachsubcatdel.gst
            # productDetail = {
            #     'productID': Product_id,
            #     'productName': productName,
            #     'productCode': ProductCode,
            #     'skuCode': skuCode,
            #     'brand': Brand,
            #     'image': str(image),
            #     'mrp': mrp,
            #     'sellingPrice': round(sellingPrice+((sellingPrice*gst)/100))

            # }
            add = ShippingAddress.objects.filter(
                id=eachbooking.shippingAddressId_id)
            for eachadd in add:
                useD = User.objects.filter(id=eachadd.user_id_id).first()
                pincode = eachadd.pincode
                flat = eachadd.flat
                address = eachadd.address
                location = eachadd.location
                landmark = eachadd.landmark
                city = eachadd.city
                district = eachadd.district
                state = eachadd.state
                name = eachadd.name
                phone = eachadd.phone
                optionalPhone = eachadd.optionalPhone
                id = useD.id
                customerID = useD.username
            ShippingAddressDetails = {
                'pincode': pincode,
                'flat': flat,
                'address': address,
                'location': location,
                'landmark': landmark,
                'city': city,
                'district': district,
                'state': state,
                'name': name,
                'phone': phone,
                'id': id,
                'customerID': customerID,
                'optionalPhone': optionalPhone,
            }

            pro = {
                'bookingDetails': bookingDetails,
                # 'productDetail': productDetail,
                'shippingAddress': ShippingAddressDetails

            }
            booking2.append(pro)
            # print(booking2)
        return Response(booking2)


class SearchBookingAPIView(views.APIView):
    def post(self, request):
        booking2 = []
        ShippingAddressDetails = []
        inputs = request.data
        query_string = inputs['search']
        booking = Booking.objects.filter(
            Q(orderID__icontains=query_string) | Q(
                OrderDate__icontains=query_string)
        ).order_by('-id')
        for eachbooking in booking:

            bookingDetails = {
                'OrderID': eachbooking.orderID,
                'orderDate': eachbooking.OrderDate,
                'productPayablePrice': eachbooking.productPayablePrice,
                'productSellingPrice': eachbooking.productSellingPrice,
                'productGST': eachbooking.productGST,
                'deliveryCharge': eachbooking.deliveryCharge,
                'walletAmount': eachbooking.walletAmount,
                'walletPoint': eachbooking.walletPoint,
                'couponDiscount': eachbooking.couponDiscount	,
                'couponCode': eachbooking.couponCode,
                'orderStatus': eachbooking.orderStatus,
                'paymentType': eachbooking.paymentType,
                'razorpayPaymentId': eachbooking.razorpayPaymentId,
                'deliveryDate': eachbooking.deliveryDate,
                'returnDate': eachbooking.returnDate,
                'returnExpairStatus': eachbooking.returnExpairStatus,
                'orderInTransitDate': eachbooking.orderInTransitDate,
                'readyForReturnDate': eachbooking.readyForReturnDate,
                'cancelDate': eachbooking.cancelDate,
                'reviewStatus': eachbooking.reviewStatus,
                'booking_id': eachbooking.id,
                'qty': eachbooking.quantity

            }

            product = Product.objects.filter(id=eachbooking.product_id_id)
            for eachproduct in product:
                productName = eachproduct.productName
                Product_id = eachproduct.id
                ProductCode = eachproduct.productCode
                skuCode = eachproduct.skuCode
                mrp = eachproduct.mrp
                sellingPrice = eachproduct.sellingPrice
                image122 = ProductImage.objects.filter(
                    productID_id=eachproduct.id)
                for eachimage in image122:
                    image = eachimage.productImage

                brand22 = ProductBrand.objects.filter(
                    id=eachproduct.productBrandID_id)
                for eachbrand in brand22:
                    Brand = eachbrand.brand_name
                subcatdel = SubCategory.objects.filter(
                    id=eachproduct.sub_cat_id_id)
                for eachsubcatdel in subcatdel:
                    gst = eachsubcatdel.gst
            productDetail = {
                'productID': Product_id,
                'productName': productName,
                'productCode': ProductCode,
                'skuCode': skuCode,
                'brand': Brand,
                'image': str(image),
                'mrp': mrp,
                'sellingPrice': round(sellingPrice)

            }
            add = ShippingAddress.objects.filter(
                id=eachbooking.shippingAddressId_id)
            for eachadd in add:
                pincode = eachadd.pincode
                flat = eachadd.flat
                address = eachadd.address
                location = eachadd.location
                landmark = eachadd.landmark
                city = eachadd.city
                district = eachadd.district
                state = eachadd.state
                name = eachadd.name
                phone = eachadd.phone
                optionalPhone = eachadd.optionalPhone
            ShippingAddressDetails = {
                'pincode': pincode,
                'flat': flat,
                'address': address,
                'location': location,
                'landmark': landmark,
                'city': city,
                'district': district,
                'state': state,
                'name': name,
                'phone': phone,
                'optionalPhone': optionalPhone,
            }

            pro = {
                'bookingDetails': bookingDetails,
                'productDetail': productDetail,
                'shippingAddress': ShippingAddressDetails,

            }
            booking2.append(pro)
        return Response(booking2)


class salesReportVendorAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        print(user_id)
        booking2 = []
        booking = Booking.objects.filter(OrderDate__range=(
            inputs['start_date'], inputs['end_date'])).order_by('-id')
        for eachbooking in booking:
            vendor = Product.objects.filter(id=eachbooking.product_id_id)
            for eachvendor in vendor:
                if eachvendor.user_id_id == user_id:
                    bookingDetails = {
                        'OrderID': eachbooking.orderID,
                        'orderDate': eachbooking.OrderDate,
                        'productPayablePrice': eachbooking.productPayablePrice,
                    }
                    users = User.objects.filter(id=eachbooking.user_id_id)

                    for user in users:
                        uname = user.name
                        uphone = user.phone
                        uemail = user.email
                    UserDetails = {
                        'name': uname,
                        'phone': uphone,
                        'email': uemail
                    }

                    pro = {
                        'bookingDetails': bookingDetails,
                        'userDetails': UserDetails
                    }
                    booking2.append(pro)
        return Response(booking2)


class taxsReportVendorAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        booking2 = []
        booking = Booking.objects.filter(OrderDate__range=(
            inputs['start_date'], inputs['end_date'])).order_by('-id')
        for eachbooking in booking:
            vendor = Product.objects.filter(id=eachbooking.product_id_id)
            for eachvendor in vendor:
                if eachvendor.user_id_id == user_id:
                    bookingDetails = {
                        'OrderID': eachbooking.orderID,
                        'orderDate': eachbooking.OrderDate,
                        'productPayablePrice': eachbooking.productPayablePrice,
                        'productGST': eachbooking.productGST,
                        'productSellingPrice': eachbooking.productSellingPrice,
                        'quantity': eachbooking.quantity
                    }
                    pro = {
                        'bookingDetails': bookingDetails,
                    }
                    booking2.append(pro)
        return Response(booking2)


class bookingHistory(views.APIView):
    def get(self, request):
        booking_history = BookingPayment.objects.all().order_by('-id')
        booking_array = []
        for book in booking_history:
            booking_payment = {
                'grandTotal': book.grandTotal,
                'paymentType': book.paymentType,
                'deliveryCharge': book.deliveryCharge,
                'walletAmount': book.walletAmount,
                'walletPoint': book.walletPoint,
                'couponDiscount': book.couponDiscount
            }
            bookings = Booking.objects.filter(bookingPaymentID=book.id)
            order_id = []
            for bk in bookings:
                booking_details = {
                    'OrderID': bk.orderID,
                    'booking_id': bk.id
                }
                order_id.append(booking_details)
            users = User.objects.filter(id=book.user_id_id)
            for user in users:
                uname = user.name
                uphone = user.phone
                uemail = user.email
                uid = user.id
                ucid = user.username

            UserDetails = {
                'id': uid,
                'name': uname,
                'phone': uphone,
                'email': uemail,
                'customerID': ucid,
            }
            details = {
                'bookingPayment': booking_payment,
                'orderId': order_id,
                'userDetails': UserDetails
            }
            booking_array.append(details)
        return Response(booking_array)


class deleveryBookingAPIView(views.APIView):
    def get(self, request):
        booking2 = []
        ShippingAddressDetails = []
        booking = Booking.objects.all().order_by('-id')
        for eachbooking in booking:

            bookingDetails = {
                'OrderID': eachbooking.orderID,
                'orderDate': eachbooking.OrderDate,
                'productPayablePrice': eachbooking.productPayablePrice,
                'productSellingPrice': eachbooking.productSellingPrice,
                'productGST': eachbooking.productGST,
                'deliveryCharge': eachbooking.deliveryCharge,
                'walletAmount': eachbooking.walletAmount,
                'walletPoint': eachbooking.walletPoint,
                'couponDiscount': eachbooking.couponDiscount	,
                'couponCode': eachbooking.couponCode,
                'orderStatus': eachbooking.orderStatus,
                'paymentType': eachbooking.paymentType,
                'razorpayPaymentId': eachbooking.razorpayPaymentId,
                'deliveryDate': eachbooking.deliveryDate,
                'returnDate': eachbooking.returnDate,
                'orderInTransitDate': eachbooking.orderInTransitDate,
                'readyForReturnDate': eachbooking.readyForReturnDate,
                'cancelDate': eachbooking.cancelDate,
                'reviewStatus': eachbooking.reviewStatus,
                'booking_id': eachbooking.id,
                'qty': eachbooking.quantity,
                'deliveryBoyId': eachbooking.deliveryBoyId,
                'returnBoyId': eachbooking.returnBoyId

            }

            product = Product.objects.filter(id=eachbooking.product_id_id)
            for eachproduct in product:
                productName = eachproduct.productName
                Product_id = eachproduct.id
                ProductCode = eachproduct.productCode
                mrp = eachproduct.mrp
                sellingPrice = eachproduct.sellingPrice
                size = eachproduct.size
                color = eachproduct.color
                image122 = ProductImage.objects.filter(
                    productID_id=eachproduct.id)
                for eachimage in image122:
                    image = eachimage.productImage

                brand22 = ProductBrand.objects.filter(
                    id=eachproduct.productBrandID_id)
                for eachbrand in brand22:
                    Brand = eachbrand.brand_name
                subcatdel = SubCategory.objects.filter(
                    id=eachproduct.sub_cat_id_id)
                for eachsubcatdel in subcatdel:
                    gst = eachsubcatdel.gst
            productDetail = {
                'productID': Product_id,
                'productName': productName,
                'productCode': ProductCode,
                'brand': Brand,
                'image': str(image),
                'mrp': mrp,
                'size': size,
                'color': color,
                'sellingPrice': round(sellingPrice)

            }
            add = ShippingAddress.objects.filter(
                id=eachbooking.shippingAddressId_id).first()
            ShippingAddressDetails = {
                'pincode': add.pincode,
                'flat': add.flat,
                'address': add.address,
                'location': add.location,
                'landmark': add.landmark,
                'city': add.city,
                'district': add.district,
                'state': add.state,
                'name': add.name,
                'phone': add.phone,
                'optionalPhone': add.optionalPhone,
            }
            delivery_boy = User.objects.filter(id=eachbooking.deliveryBoyId).first()
            if delivery_boy:
                DeliveryboyDetails = {
                    'name': delivery_boy.dname,
                    'phone': delivery_boy.dphone,
                }
            else:
                DeliveryboyDetails = {}
            return_boy = User.objects.filter(id=eachbooking.returnBoyId).first()
            if return_boy:
                ReturnboyDetails = {
                    'name': return_boy.rname,
                    'phone': return_boy.rphone,
                }
            else:
                ReturnboyDetails = {}
            users = User.objects.filter(id=eachbooking.user_id_id).first()
            UserDetails = {
                'name': users.uname,
                'phone': users.uphone,
                'email': users.uemail
            }

            pro = {
                'bookingDetails': bookingDetails,
                'productDetail': productDetail,
                'shippingAddress': ShippingAddressDetails,
                'deliveryBoy': DeliveryboyDetails,
                'returnBoy': ReturnboyDetails,
                'billingAddress': ShippingAddressDetails,
                'userDetails': UserDetails
            }
            booking2.append(pro)
        return Response(booking2)


class deleveryReportAPIView(views.APIView):
    def get(self, request, id):
        boy_id = id
        booking2 = []
        ShippingAddressDetails = []
        booking = Booking.objects.filter(deliveryBoyId=boy_id).order_by('-id')
        total_booking = Booking.objects.filter(deliveryBoyId=boy_id).count()
        delever_booking = Booking.objects.filter(
            deliveryBoyId=boy_id, orderStatus__gte=3).count()
        for eachbooking in booking:

            bookingDetails = {
                'OrderID': eachbooking.orderID,
                'orderDate': eachbooking.OrderDate,
                'productPayablePrice': eachbooking.productPayablePrice,
                'orderStatus': eachbooking.orderStatus,
                'deliveryDate': eachbooking.deliveryDate

            }

            add = ShippingAddress.objects.filter(
                id=eachbooking.shippingAddressId_id)
            for eachadd in add:
                pincode = eachadd.pincode
                city = eachadd.city

            ShippingAddressDetails = {
                'pincode': pincode,
                'city': city,
            }
            delivery_boy = User.objects.filter(id=eachbooking.deliveryBoyId)
            if delivery_boy:
                for dely in delivery_boy:
                    dname = dely.name
                    dphone = dely.phone
                DeliveryboyDetails = {
                    'name': dname,
                }
            else:
                DeliveryboyDetails = {}

            pro = {
                'bookingDetails': bookingDetails,
                'shippingAddress': ShippingAddressDetails,
                'deliveryBoy': DeliveryboyDetails,
                'total_booking': total_booking,
                'delivery_booking': delever_booking

            }
            booking2.append(pro)
        return Response(booking2)


class returnReportBookingAPIView(views.APIView):
    def get(self, request, id):
        boy_id = id
        booking2 = []
        ShippingAddressDetails = []
        booking = Booking.objects.filter(returnBoyId=boy_id).order_by('-id')
        total_booking = Booking.objects.filter(returnBoyId=boy_id).count()
        delever_booking = Booking.objects.filter(
            returnBoyId=boy_id, orderStatus__gte=7).count()
        for eachbooking in booking:

            bookingDetails = {
                'OrderID': eachbooking.orderID,
                'orderDate': eachbooking.OrderDate,
                'productPayablePrice': eachbooking.productPayablePrice,
                'orderStatus': eachbooking.orderStatus,
                'returnDate': eachbooking.returnDate
            }

            add = ShippingAddress.objects.filter(
                id=eachbooking.shippingAddressId_id)
            for eachadd in add:
                pincode = eachadd.pincode
                city = eachadd.city

            ShippingAddressDetails = {
                'pincode': pincode,
                'city': city,
            }
            delivery_boy = User.objects.filter(id=eachbooking.returnBoyId)
            if delivery_boy:
                for dely in delivery_boy:
                    dname = dely.name
                    dphone = dely.phone
                DeliveryboyDetails = {
                    'name': dname,
                }
            else:
                DeliveryboyDetails = {}

            pro = {
                'bookingDetails': bookingDetails,
                'shippingAddress': ShippingAddressDetails,
                'returnBoy': DeliveryboyDetails,
                'total_booking': total_booking,
                'delivery_booking': delever_booking

            }
            booking2.append(pro)
        return Response(booking2)


class deliveryBoyBookingAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id

        booking2 = []
        ShippingAddressDetails = []
        booking = Booking.objects.all().order_by('-id')
        for eachbooking in booking:
            vendor = Product.objects.filter(id=eachbooking.product_id_id)
            for eachvendor in vendor:
                if eachvendor.deliveryBoyId == user_id:

                    bookingDetails = {
                        'OrderID': eachbooking.orderID,
                        'orderDate': eachbooking.OrderDate,
                        'productPayablePrice': eachbooking.productPayablePrice,
                        'productSellingPrice': eachbooking.productSellingPrice,
                        'productGST': eachbooking.productGST,
                        'deliveryCharge': eachbooking.deliveryCharge,
                        'walletAmount': eachbooking.walletAmount,
                        'couponDiscount': eachbooking.couponDiscount	,
                        'couponCode': eachbooking.couponCode,
                        'orderStatus': eachbooking.orderStatus,
                        'paymentType': eachbooking.paymentType,
                        'razorpayPaymentId': eachbooking.razorpayPaymentId,
                        'deliveryDate': eachbooking.deliveryDate,
                        'returnDate': eachbooking.returnDate,
                        'returnExpairStatus': eachbooking.returnExpairStatus,
                        'redeemStatus': eachbooking.redeemStatus,
                        'orderInTransitDate': eachbooking.orderInTransitDate,
                        'readyForReturnDate': eachbooking.readyForReturnDate,
                        'cancelDate': eachbooking.cancelDate,
                        'reviewStatus': eachbooking.reviewStatus,
                        'booking_id': eachbooking.id,
                        'qty': eachbooking.quantity

                    }

                    product = Product.objects.filter(
                        id=eachbooking.product_id_id)
                    for eachproduct in product:
                        productName = eachproduct.productName
                        Product_id = eachproduct.id
                        ProductCode = eachproduct.productCode
                        mrp = eachproduct.mrp
                        sellingPrice = eachproduct.sellingPrice
                        image122 = ProductImage.objects.filter(
                            productID_id=eachproduct.id)
                        for eachimage in image122:
                            image = eachimage.productImage

                        brand22 = ProductBrand.objects.filter(
                            id=eachproduct.productBrandID_id)
                        for eachbrand in brand22:
                            Brand = eachbrand.brand_name
                        subcatdel = SubCategory.objects.filter(
                            id=eachproduct.sub_cat_id_id)
                        for eachsubcatdel in subcatdel:
                            gst = eachsubcatdel.gst
                            comm = eachsubcatdel.commission
                    productDetail = {
                        'productID': Product_id,
                        'productName': productName,
                        'productCode': ProductCode,
                        'brand': Brand,
                        'image': str(image),
                        'mrp': mrp,
                        'sellingPrice': round(sellingPrice),
                        'comm': round((sellingPrice*comm)/100)
                    }
                    add = ShippingAddress.objects.filter(
                        id=eachbooking.shippingAddressId_id)
                    for eachadd in add:
                        pincode = eachadd.pincode
                        flat = eachadd.flat
                        address = eachadd.address
                        location = eachadd.location
                        landmark = eachadd.landmark
                        city = eachadd.city
                        district = eachadd.district
                        state = eachadd.state
                        name = eachadd.name
                        phone = eachadd.phone
                        optionalPhone = eachadd.optionalPhone
                    ShippingAddressDetails = {
                        'pincode': pincode,
                        'flat': flat,
                        'address': address,
                        'location': location,
                        'landmark': landmark,
                        'city': city,
                        'district': district,
                        'state': state,
                        'name': name,
                        'phone': phone,
                        'optionalPhone': optionalPhone,
                    }

                    pro = {
                        'bookingDetails': bookingDetails,
                        'productDetail': productDetail,
                        'shippingAddress': ShippingAddressDetails,

                    }
                    booking2.append(pro)

        return Response(booking2)


class deliveryBoyPendingBookingAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id

        booking2 = []
        ShippingAddressDetails = []
        booking = Booking.objects.filter(Q(orderStatus=1) | Q(orderStatus=2) | Q(
            orderStatus=3), deliveryBoyId=user_id).order_by('-id')
        for eachbooking in booking:
            vendor = Product.objects.filter(id=eachbooking.product_id_id)
            for eachvendor in vendor:

                bookingDetails = {
                    'OrderID': eachbooking.orderID,
                    'orderDate': eachbooking.OrderDate,
                    'productPayablePrice': eachbooking.productPayablePrice,
                    'productSellingPrice': eachbooking.productSellingPrice,
                    'productGST': eachbooking.productGST,
                    'deliveryCharge': eachbooking.deliveryCharge,
                    'walletAmount': eachbooking.walletAmount,
                    'couponDiscount': eachbooking.couponDiscount	,
                    'couponCode': eachbooking.couponCode,
                    'orderStatus': eachbooking.orderStatus,
                    'paymentType': eachbooking.paymentType,
                    'razorpayPaymentId': eachbooking.razorpayPaymentId,
                    'deliveryDate': eachbooking.deliveryDate,
                    'returnDate': eachbooking.returnDate,
                    'returnExpairStatus': eachbooking.returnExpairStatus,
                    'redeemStatus': eachbooking.redeemStatus,
                    'orderInTransitDate': eachbooking.orderInTransitDate,
                    'readyForReturnDate': eachbooking.readyForReturnDate,
                    'cancelDate': eachbooking.cancelDate,
                    'reviewStatus': eachbooking.reviewStatus,
                    'booking_id': eachbooking.id,
                    'qty': eachbooking.quantity

                }

                product = Product.objects.filter(id=eachbooking.product_id_id)
                for eachproduct in product:
                    productName = eachproduct.productName
                    Product_id = eachproduct.id
                    ProductCode = eachproduct.productCode
                    mrp = eachproduct.mrp
                    sellingPrice = eachproduct.sellingPrice
                    image122 = ProductImage.objects.filter(
                        productID_id=eachproduct.id)
                    for eachimage in image122:
                        image = eachimage.productImage

                    brand22 = ProductBrand.objects.filter(
                        id=eachproduct.productBrandID_id)
                    for eachbrand in brand22:
                        Brand = eachbrand.brand_name
                    subcatdel = SubCategory.objects.filter(
                        id=eachproduct.sub_cat_id_id)
                    for eachsubcatdel in subcatdel:
                        gst = eachsubcatdel.gst
                        comm = eachsubcatdel.commission
                productDetail = {
                    'productID': Product_id,
                    'productName': productName,
                    'productCode': ProductCode,
                    'brand': Brand,
                    'image': str(image),
                    'mrp': mrp,
                    'sellingPrice': round(sellingPrice),
                    'comm': round((sellingPrice*comm)/100)
                }
                add = ShippingAddress.objects.filter(
                    id=eachbooking.shippingAddressId_id)
                for eachadd in add:
                    pincode = eachadd.pincode
                    flat = eachadd.flat
                    address = eachadd.address
                    location = eachadd.location
                    landmark = eachadd.landmark
                    city = eachadd.city
                    district = eachadd.district
                    state = eachadd.state
                    name = eachadd.name
                    phone = eachadd.phone
                    optionalPhone = eachadd.optionalPhone
                ShippingAddressDetails = {
                    'pincode': pincode,
                    'flat': flat,
                    'address': address,
                    'location': location,
                    'landmark': landmark,
                    'city': city,
                    'district': district,
                    'state': state,
                    'name': name,
                    'phone': phone,
                    'optionalPhone': optionalPhone,
                }

                pro = {
                    'bookingDetails': bookingDetails,
                    'productDetail': productDetail,
                    'shippingAddress': ShippingAddressDetails,

                }
                booking2.append(pro)

        return Response(booking2)


class deliveryBoyCompleteBookingAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id

        booking2 = []
        ShippingAddressDetails = []
        booking = Booking.objects.filter(
            orderStatus=4, deliveryBoyId=user_id).order_by('-id')
        for eachbooking in booking:
            vendor = Product.objects.filter(id=eachbooking.product_id_id)
            for eachvendor in vendor:

                bookingDetails = {
                    'OrderID': eachbooking.orderID,
                    'orderDate': eachbooking.OrderDate,
                    'productPayablePrice': eachbooking.productPayablePrice,
                    'productSellingPrice': eachbooking.productSellingPrice,
                    'productGST': eachbooking.productGST,
                    'deliveryCharge': eachbooking.deliveryCharge,
                    'walletAmount': eachbooking.walletAmount,
                    'couponDiscount': eachbooking.couponDiscount	,
                    'couponCode': eachbooking.couponCode,
                    'orderStatus': eachbooking.orderStatus,
                    'paymentType': eachbooking.paymentType,
                    'razorpayPaymentId': eachbooking.razorpayPaymentId,
                    'deliveryDate': eachbooking.deliveryDate,
                    'returnDate': eachbooking.returnDate,
                    'returnExpairStatus': eachbooking.returnExpairStatus,
                    'redeemStatus': eachbooking.redeemStatus,
                    'orderInTransitDate': eachbooking.orderInTransitDate,
                    'readyForReturnDate': eachbooking.readyForReturnDate,
                    'cancelDate': eachbooking.cancelDate,
                    'reviewStatus': eachbooking.reviewStatus,
                    'booking_id': eachbooking.id,
                    'qty': eachbooking.quantity

                }

                product = Product.objects.filter(id=eachbooking.product_id_id)
                for eachproduct in product:
                    productName = eachproduct.productName
                    Product_id = eachproduct.id
                    ProductCode = eachproduct.productCode
                    mrp = eachproduct.mrp
                    sellingPrice = eachproduct.sellingPrice
                    image122 = ProductImage.objects.filter(
                        productID_id=eachproduct.id)
                    for eachimage in image122:
                        image = eachimage.productImage

                    brand22 = ProductBrand.objects.filter(
                        id=eachproduct.productBrandID_id)
                    for eachbrand in brand22:
                        Brand = eachbrand.brand_name
                    subcatdel = SubCategory.objects.filter(
                        id=eachproduct.sub_cat_id_id)
                    for eachsubcatdel in subcatdel:
                        gst = eachsubcatdel.gst
                        comm = eachsubcatdel.commission
                productDetail = {
                    'productID': Product_id,
                    'productName': productName,
                    'productCode': ProductCode,
                    'brand': Brand,
                    'image': str(image),
                    'mrp': mrp,
                    'sellingPrice': round(sellingPrice),
                    'comm': round((sellingPrice*comm)/100)
                }
                add = ShippingAddress.objects.filter(
                    id=eachbooking.shippingAddressId_id)
                for eachadd in add:
                    pincode = eachadd.pincode
                    flat = eachadd.flat
                    address = eachadd.address
                    location = eachadd.location
                    landmark = eachadd.landmark
                    city = eachadd.city
                    district = eachadd.district
                    state = eachadd.state
                    name = eachadd.name
                    phone = eachadd.phone
                    optionalPhone = eachadd.optionalPhone
                ShippingAddressDetails = {
                    'pincode': pincode,
                    'flat': flat,
                    'address': address,
                    'location': location,
                    'landmark': landmark,
                    'city': city,
                    'district': district,
                    'state': state,
                    'name': name,
                    'phone': phone,
                    'optionalPhone': optionalPhone,
                }

                pro = {
                    'bookingDetails': bookingDetails,
                    'productDetail': productDetail,
                    'shippingAddress': ShippingAddressDetails,

                }
                booking2.append(pro)

        return Response(booking2)


class deliveryBoyCompleteReturnBookingAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id

        booking2 = []
        ShippingAddressDetails = []
        booking = Booking.objects.filter(
            orderStatus=8, returnBoyId=user_id).order_by('-id')
        for eachbooking in booking:
            vendor = Product.objects.filter(id=eachbooking.product_id_id)
            for eachvendor in vendor:

                bookingDetails = {
                    'OrderID': eachbooking.orderID,
                    'orderDate': eachbooking.OrderDate,
                    'productPayablePrice': eachbooking.productPayablePrice,
                    'productSellingPrice': eachbooking.productSellingPrice,
                    'productGST': eachbooking.productGST,
                    'deliveryCharge': eachbooking.deliveryCharge,
                    'walletAmount': eachbooking.walletAmount,
                    'couponDiscount': eachbooking.couponDiscount	,
                    'couponCode': eachbooking.couponCode,
                    'orderStatus': eachbooking.orderStatus,
                    'paymentType': eachbooking.paymentType,
                    'razorpayPaymentId': eachbooking.razorpayPaymentId,
                    'deliveryDate': eachbooking.deliveryDate,
                    'returnDate': eachbooking.returnDate,
                    'returnExpairStatus': eachbooking.returnExpairStatus,
                    'redeemStatus': eachbooking.redeemStatus,
                    'orderInTransitDate': eachbooking.orderInTransitDate,
                    'readyForReturnDate': eachbooking.readyForReturnDate,
                    'cancelDate': eachbooking.cancelDate,
                    'reviewStatus': eachbooking.reviewStatus,
                    'booking_id': eachbooking.id,
                    'qty': eachbooking.quantity

                }

                product = Product.objects.filter(id=eachbooking.product_id_id)
                for eachproduct in product:
                    productName = eachproduct.productName
                    Product_id = eachproduct.id
                    ProductCode = eachproduct.productCode
                    mrp = eachproduct.mrp
                    sellingPrice = eachproduct.sellingPrice
                    image122 = ProductImage.objects.filter(
                        productID_id=eachproduct.id)
                    for eachimage in image122:
                        image = eachimage.productImage

                    brand22 = ProductBrand.objects.filter(
                        id=eachproduct.productBrandID_id)
                    for eachbrand in brand22:
                        Brand = eachbrand.brand_name
                    subcatdel = SubCategory.objects.filter(
                        id=eachproduct.sub_cat_id_id)
                    for eachsubcatdel in subcatdel:
                        gst = eachsubcatdel.gst
                        comm = eachsubcatdel.commission
                productDetail = {
                    'productID': Product_id,
                    'productName': productName,
                    'productCode': ProductCode,
                    'brand': Brand,
                    'image': str(image),
                    'mrp': mrp,
                    'sellingPrice': round(sellingPrice),
                    'comm': round((sellingPrice*comm)/100)
                }
                add = ShippingAddress.objects.filter(
                    id=eachbooking.shippingAddressId_id)
                for eachadd in add:
                    pincode = eachadd.pincode
                    flat = eachadd.flat
                    address = eachadd.address
                    location = eachadd.location
                    landmark = eachadd.landmark
                    city = eachadd.city
                    district = eachadd.district
                    state = eachadd.state
                    name = eachadd.name
                    phone = eachadd.phone
                    optionalPhone = eachadd.optionalPhone
                ShippingAddressDetails = {
                    'pincode': pincode,
                    'flat': flat,
                    'address': address,
                    'location': location,
                    'landmark': landmark,
                    'city': city,
                    'district': district,
                    'state': state,
                    'name': name,
                    'phone': phone,
                    'optionalPhone': optionalPhone,
                }

                pro = {
                    'bookingDetails': bookingDetails,
                    'productDetail': productDetail,
                    'shippingAddress': ShippingAddressDetails,

                }
                booking2.append(pro)

        return Response(booking2)


class deliveryBoyPendingReturnBookingAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id

        booking2 = []
        ShippingAddressDetails = []
        booking = Booking.objects.filter(Q(orderStatus=5) | Q(orderStatus=6) | Q(
            orderStatus=7), returnBoyId=user_id).order_by('-id')
        for eachbooking in booking:
            vendor = Product.objects.filter(id=eachbooking.product_id_id)
            for eachvendor in vendor:

                bookingDetails = {
                    'OrderID': eachbooking.orderID,
                    'orderDate': eachbooking.OrderDate,
                    'productPayablePrice': eachbooking.productPayablePrice,
                    'productSellingPrice': eachbooking.productSellingPrice,
                    'productGST': eachbooking.productGST,
                    'deliveryCharge': eachbooking.deliveryCharge,
                    'walletAmount': eachbooking.walletAmount,
                    'couponDiscount': eachbooking.couponDiscount	,
                    'couponCode': eachbooking.couponCode,
                    'orderStatus': eachbooking.orderStatus,
                    'paymentType': eachbooking.paymentType,
                    'razorpayPaymentId': eachbooking.razorpayPaymentId,
                    'deliveryDate': eachbooking.deliveryDate,
                    'returnDate': eachbooking.returnDate,
                    'returnExpairStatus': eachbooking.returnExpairStatus,
                    'redeemStatus': eachbooking.redeemStatus,
                    'orderInTransitDate': eachbooking.orderInTransitDate,
                    'readyForReturnDate': eachbooking.readyForReturnDate,
                    'cancelDate': eachbooking.cancelDate,
                    'reviewStatus': eachbooking.reviewStatus,
                    'booking_id': eachbooking.id,
                    'qty': eachbooking.quantity

                }

                product = Product.objects.filter(id=eachbooking.product_id_id)
                for eachproduct in product:
                    productName = eachproduct.productName
                    Product_id = eachproduct.id
                    ProductCode = eachproduct.productCode
                    mrp = eachproduct.mrp
                    sellingPrice = eachproduct.sellingPrice
                    image122 = ProductImage.objects.filter(
                        productID_id=eachproduct.id)
                    for eachimage in image122:
                        image = eachimage.productImage

                    brand22 = ProductBrand.objects.filter(
                        id=eachproduct.productBrandID_id)
                    for eachbrand in brand22:
                        Brand = eachbrand.brand_name
                    subcatdel = SubCategory.objects.filter(
                        id=eachproduct.sub_cat_id_id)
                    for eachsubcatdel in subcatdel:
                        gst = eachsubcatdel.gst
                        comm = eachsubcatdel.commission
                productDetail = {
                    'productID': Product_id,
                    'productName': productName,
                    'productCode': ProductCode,
                    'brand': Brand,
                    'image': str(image),
                    'mrp': mrp,
                    'sellingPrice': round(sellingPrice),
                    'comm': round((sellingPrice*comm)/100)
                }
                add = ShippingAddress.objects.filter(
                    id=eachbooking.shippingAddressId_id)
                for eachadd in add:
                    pincode = eachadd.pincode
                    flat = eachadd.flat
                    address = eachadd.address
                    location = eachadd.location
                    landmark = eachadd.landmark
                    city = eachadd.city
                    district = eachadd.district
                    state = eachadd.state
                    name = eachadd.name
                    phone = eachadd.phone
                    optionalPhone = eachadd.optionalPhone
                ShippingAddressDetails = {
                    'pincode': pincode,
                    'flat': flat,
                    'address': address,
                    'location': location,
                    'landmark': landmark,
                    'city': city,
                    'district': district,
                    'state': state,
                    'name': name,
                    'phone': phone,
                    'optionalPhone': optionalPhone,
                }

                pro = {
                    'bookingDetails': bookingDetails,
                    'productDetail': productDetail,
                    'shippingAddress': ShippingAddressDetails,

                }
                booking2.append(pro)

        return Response(booking2)


class userSingleBookingOrderIdAPIView(views.APIView):
    def get(self, request, id):
        b_id = id
        booking_id = 0
        status = 0
        booking = Booking.objects.filter(orderID=b_id).order_by('-id')
        for eachbooking in booking:
            booking_id = eachbooking.id
            if eachbooking.orderStatus <= 4:
                status = 1
            else:
                status = 3

        pro = {
            'booking_id': booking_id,
            'booking_status': status,
            'valid': True,
        }

        if len(booking) == 0:
            status = 0
            booking_id = 0
            pro = {
                'booking_id': booking_id,
                'booking_status': status,
                'valid': False,
            }

        return Response(pro)


def get_unique_numbers(numbers):

    list_of_unique_numbers = []

    unique_numbers = set(numbers)

    for number in unique_numbers:
        list_of_unique_numbers.append(number)

    return list_of_unique_numbers
