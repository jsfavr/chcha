from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, views
from .serializers import ReviewSerializer, SubscribeSerializer, InventoryTransactionSerializer, NotifyMeSerializer, SettingsSerializer, paymentOptionSerializer
from rest_framework import permissions, status
from .models import Review, Subscribe, InventoryTransaction, NotifyMe, Settings, paymentOption
from rest_framework.response import Response
from product.models import Product, ProductBrand, ProductImage
from django.core import serializers
from product.permissions import IsOwner
from booking.models import Booking
from category.models import SubCategory, Category, SubSubCategory
from wallet.models import Wallet, WalletTransaction
from django.db.models import Sum, Count
from authentication.models import User
from datetime import date
from django.db.models.functions import ExtractYear, ExtractMonth
import requests
import json
from address.models import DeliveryPincode
from django.db.models import Q
from wallet.views import smsSend
from django.db import models
from django.db.models import Func
# Create your views here.


class ReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class ReviewAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class SubscribeAPIView(ListCreateAPIView):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class SubscribeAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class InventoryTransactionAPIView(ListCreateAPIView):
    serializer_class = InventoryTransactionSerializer
    queryset = InventoryTransaction.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class InventoryTransactionAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = InventoryTransactionSerializer
    queryset = InventoryTransaction.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class AddStock(views.APIView):
    def post(self, request):
        inputs = request.data
        product = Product.objects.filter(id=inputs['product_id'])
        #productDetails=serializers.serialize('json', product)
        for eachProd in product:
            totalStock = int(eachProd.totalStock)+int(inputs['quantity'])
            availableStock = int(eachProd.availableStock) + \
                int(inputs['quantity'])

        Product.objects.filter(id=inputs['product_id']).update(
            totalStock=totalStock, availableStock=availableStock)

        product_trans_data = InventoryTransaction.objects.create(
            product_id_id=inputs['product_id'], quantity=inputs['quantity'], remarks='ADD STOCK', transactionType='CREDIT', transactionID=inputs['transactionID'], afterTransactionQuantity=availableStock)
        product_trans_data.save()
        ###################SMS###############
        mobile_no = []
        noti = NotifyMe.objects.filter(product_id_id=inputs['product_id'])
        product1 = Product.objects.filter(id=inputs['product_id']).first()
        for eachNoti in noti:
            phon = User.objects.filter(id=eachNoti.user_id_id).first()
            phoneNo = phon.phone
            mobile_no.append(phoneNo)
        number = ",".join(set(mobile_no))
        print('desfrtyurewertyurewq')
        print(number)
        msg = 'Product Back in Store : You have watting for '+product1.productName + \
            ' product back in our store. It is in stock now. Only ' + \
            str(availableStock)+' items available. Hurry Up.'

        template_id = ''
        # sms_body = inputs['msg']
        # phone_no = inputs['phone_no']
        # smsSend(number, msg, template_id)

        # response = requests.get(
        #     "http://weberleads.in/http-tokenkeyapi.php?authentic-key=3134696e7374616e745f6765747761793631321586003895&senderid=INGWAY&route=2&number="+number+"&message="+msg)

        return Response({'product': 'Successfully Added'}, status=status.HTTP_200_OK)


class userReviewAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        user_id = self.request.user.id
        inputs = request.data
        product = Product.objects.filter(id=inputs['product_id'])
        for eachProd in product:
            totalReview = eachProd.totalReview
            avgReview = eachProd.avgReview

        newTotalReview = int(totalReview)+int(1)
        newAvgReview = round(
            ((avgReview*totalReview)+int(inputs['ratting']))/newTotalReview, 2)
        Product.objects.filter(id=inputs['product_id']).update(
            totalReview=newTotalReview, avgReview=newAvgReview)
        Booking.objects.filter(id=inputs['booking_id']).update(reviewStatus=1)
        reasonCreate = Review.objects.create(
            user_id_id=user_id, product_id_id=inputs['product_id'],booking_id=inputs['booking_id'], ratting=inputs['ratting'], details=inputs['review_msg'])

        newrel = {
            'status': 'Review save successfully',
            'code': 1,
        }
        return Response(newrel)

class getReview(views.APIView):
    def post(self, request):
        inputs=request.data
        reviewDetails=Review.objects.filter(booking_id=inputs['booking_id']).first()
        if reviewDetails:
            newArr={
                'id':reviewDetails.id,
                'ratting' :reviewDetails.ratting,
                'message':reviewDetails.details
            }
        else:
            newArr={}
        return Response(newArr)

class userSearchAPIView(views.APIView):
    def post(self, request):
        inputs = request.data
        product = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1, productName__icontains=inputs['name'])[:5]
        productArray = []
        for eachProd in product:
            brand = ProductBrand.objects.filter(id=eachProd.productBrandID_id)
            for eachbrand in brand:
                brandName = eachbrand.brand_name
            image = ProductImage.objects.filter(productID_id=eachProd.id)[:1]
            for eachimage in image:
                productImage = eachimage.productImage
            sub = SubCategory.objects.filter(id=eachProd.sub_cat_id_id)
            for eachsub in sub:
                gst = eachsub.gst
            id = eachProd.id
            name = eachProd.productName
            mrp = eachProd.mrp
            sellingPrice = eachProd.sellingPrice + \
                ((eachProd.sellingPrice*gst)/100)
            newrel = {
                'id': id,
                'name': name,
                'brand': brandName,
                'productImage': str(productImage),
                'mrp': mrp,
                'sellingPrice': sellingPrice,
            }
            productArray.append(newrel)
        return Response(productArray)


class vendorRedeemAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        booking = Booking.objects.filter(id=inputs['booking_id'])
        for eachBooking in booking:
            payablePrice = eachBooking.productPayablePrice
            qty = eachBooking.quantity
            productID = eachBooking.product_id_id
            orderID = eachBooking.orderID
            product = Product.objects.filter(id=productID)
            custID = eachBooking.user_id_id
            for eachProduct in product:
                subCatID = eachProduct.sub_cat_id_id
                sellingPrice = eachProduct.sellingPrice
                sub_cat = SubCategory.objects.filter(id=subCatID)
                for eachSub_cat in sub_cat:
                    adminCommission = eachSub_cat.commission
                    gst = eachSub_cat.gst

        commission = round((sellingPrice*adminCommission)/100)*qty
        reddemPrice = payablePrice-commission
        wallet = Wallet.objects.filter(user_id_id=user_id)
        for eachWallet in wallet:
            # print(eachWallet)
            currentBalance = eachWallet.amount
            # print(currentBalance)

            updatedWalletBalance = currentBalance+reddemPrice
        bookingUpdate = Booking.objects.filter(
            id=inputs['booking_id']).update(redeemStatus=1)
        walletUpdate = Wallet.objects.filter(
            user_id_id=user_id).update(amount=updatedWalletBalance)
        WalletTransCreate = WalletTransaction.objects.create(
            user_id_id=user_id, transactionAmount=reddemPrice, afterTransactionAmount=updatedWalletBalance, remarks='Order Redeem - '+orderID, transactionType='CREDIT')

        Boo = Booking.objects.filter(user_id_id=custID).first()
        if inputs['booking_id'] == Boo.id:
            userdetails = User.objects.filter(id=custID)
            for eachUser in userdetails:
                referCode = eachUser.refer_code

            if referCode != None:
                userdetails1 = User.objects.filter(username=referCode)
                for eachUser1 in userdetails1:
                    referUserId = eachUser1.id
                wallet2 = Wallet.objects.filter(user_id_id=referUserId)
                for eachWallet2 in wallet2:
                    currentBalance2 = eachWallet2.amount
                reddemPrice2 = 100
                updatedWalletBalance2 = currentBalance2+reddemPrice2
                walletUpdate = Wallet.objects.filter(
                    user_id_id=referUserId).update(amount=updatedWalletBalance2)
                WalletTransCreate = WalletTransaction.objects.create(
                    user_id_id=referUserId, transactionAmount=reddemPrice2, afterTransactionAmount=updatedWalletBalance2, remarks='Refer Cashback', transactionType='CREDIT')

        return Response({'status': 'Redeem Successful'}, status=status.HTTP_200_OK)


class AdminHighRattingAPIView(views.APIView):
    def get(self, request):
        booking = Review.objects.all().order_by('-ratting')[:100]
        modifiedrel = []

        for book in booking:
            product = Product.objects.filter(id=book.product_id_id)[:13]
            for eachrel in product:
                det = Booking.objects.filter(product_id_id=eachrel.id).count()
                newrel = {
                    'name': eachrel.productName,
                    'code': eachrel.productCode,
                    'id': eachrel.id,
                    'ratting': book.ratting,
                    'comments': book.details
                }
                modifiedrel.append(newrel)
        return Response(modifiedrel)


class AdminLowRattingAPIView(views.APIView):
    def get(self, request):
        booking = Review.objects.all().order_by('ratting')[:100]
        modifiedrel = []

        for book in booking:
            product = Product.objects.filter(id=book.product_id_id)[:13]
            for eachrel in product:
                det = Booking.objects.filter(product_id_id=eachrel.id).count()
                newrel = {
                    'name': eachrel.productName,
                    'code': eachrel.productCode,
                    'id': eachrel.id,
                    'ratting': book.ratting,
                    'comments': book.details
                }
                modifiedrel.append(newrel)
        return Response(modifiedrel)


class AdminHomeAPIView(views.APIView):
    def get(self, request):
        modifiedrel = []
        top = Product.objects.all().order_by('-orderCount')[:1]
        for topProduct in top:
            name = topProduct.productName
            count = topProduct.orderCount
        topSelling = {
            'name': name,
            'count': count,
        }
        view = Product.objects.all().order_by('-viewCount')[:1]
        for topview in view:
            name = topview.productName
            count = topview.orderCount
        mostView = {
            'name': name,
            'count': count,
        }
        review = Product.objects.all().order_by('-avgReview')[:1]
        for topreview in review:
            name = topreview.productName
            count = topreview.avgReview
        mostReview = {
            'name': name,
            'count': count,
        }
        rea = Product.objects.all().count()
        rea2 = Product.objects.all().aggregate(Sum('avgReview'))
        mostRatting = {
            'rate': round(rea2['avgReview__sum']/rea, 1),
        }
        vendor = User.objects.filter(role_id=2).count()
        booking = Booking.objects.all().count()
        product = Product.objects.all().count()
        delivary = User.objects.filter(subscriptionStatus=1).count()
        total = {
            'booking': booking,
            'product': product,
            'vendor': vendor,
            'delivary': delivary

        }

        graph = Booking.objects.annotate(
            year=ExtractYear('OrderDate'),
            month=ExtractMonth('OrderDate'),
        ).values('year', 'month').annotate(count=Count('pk'))

        data = {
            'topSelling': topSelling,
            'mostView': mostView,
            'mostRatting': mostRatting,
            'mostReview': mostReview,
            'total': total,

        }

        return Response(data)


class VendorHomeAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id
        delivered = 0
        cancel = 0
        returnB = 0
        pending = 0
        print(delivered)
        product = Product.objects.filter(user_id=user_id).count()
        top = Product.objects.filter(
            user_id=user_id).order_by('-orderCount')[:1]
        for topProduct in top:
            name = topProduct.productName
            count = topProduct.orderCount
        topSelling = {
            'name': name,
            'count': count,
        }
        view = Product.objects.filter(
            user_id=user_id).order_by('-viewCount')[:1]
        for topview in view:
            name = topview.productName
            count = topview.orderCount
        mostView = {
            'name': name,
            'count': count,
        }
        review = Product.objects.filter(
            user_id=user_id).order_by('-avgReview')[:1]
        for topreview in review:
            name = topreview.productName
            count = topreview.avgReview
        mostReview = {
            'name': name,
            'count': count,
        }
        booking = Booking.objects.all()
        for eachBooking in booking:
            p = Product.objects.filter(
                id=eachBooking.product_id_id, user_id=user_id).count()
            if p:
                if eachBooking.orderStatus == 4:
                    # print(delivered)
                    delivered = int(delivered)+1
                if eachBooking.orderStatus == 8:
                    # print(returnB)
                    returnB = int(returnB)+int(1)
                if eachBooking.orderStatus == 9:
                    # print(cancel)
                    cancel = int(cancel)+int(1)

                if eachBooking.orderStatus == 1:
                    # print(cancel)
                    pending = int(pending)+int(1)

        data = {
            'totalProduct': product,
            'delivery': delivered,
            'cancel': cancel,
            'return': returnB,
            'pending': pending,
            'topSelling': topSelling,
            'mostView': mostView,
            'mostReview': mostReview,

        }
        return Response(data)


class usersearchByCodeAPIView(views.APIView):
    def post(self, request):
        inputs = request.data
        product = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1, productName__contains=inputs['name'])[:5]
        productArray = []
        for eachProd in product:
            brand = ProductBrand.objects.filter(id=eachProd.productBrandID_id)
            for eachbrand in brand:
                brandName = eachbrand.brand_name
            image = ProductImage.objects.filter(productID_id=eachProd.id)[:1]
            for eachimage in image:
                productImage = eachimage.productImage
            sub = SubCategory.objects.filter(id=eachProd.sub_cat_id_id)
            for eachsub in sub:
                gst = eachsub.gst
            id = eachProd.id
            name = eachProd.productName
            mrp = eachProd.mrp
            code = eachProd.productCode

            sellingPrice = eachProd.sellingPrice + \
                ((eachProd.sellingPrice*gst)/100)
            newrel = {
                'id': id,
                'name': name,
                'brand': brandName,
                'productImage': str(productImage),
                'mrp': mrp,
                'sellingPrice': sellingPrice,
                'code': code,
                'type': 'product',

            }
            productArray.append(newrel)

        brand = ProductBrand.objects.filter(
            brand_name__contains=inputs['name'])[:3]
        for eachBrand in brand:
            newrel = {
                'id': eachBrand.id,
                'name': eachBrand.brand_name,
                'brand': 'Brand',
                'productImage': str(eachBrand.brand_logo),
                'mrp': '',
                'sellingPrice': '',
                'code': '',
                'type': 'brand',
            }
            productArray.append(newrel)

        subsubcat = SubSubCategory.objects.filter(
            sub_sub_cat_name__contains=inputs['name'])[:2]
        for eachsubsubcat in subsubcat:
            subCat = SubCategory.objects.filter(
                id=eachsubsubcat.sub_cat_id_id).first()
            Cat = Category.objects.filter(id=subCat.cat_id_id).first()
            newrel = {
                'id': eachsubsubcat.id,
                'name': eachsubsubcat.sub_sub_cat_name,
                'brand': subCat.sub_cat_name,
                'productImage': str(eachsubsubcat.sub_sub_cat_icon),
                'mrp': '',
                'sellingPrice': '',
                'code': '',
                'sub_id': subCat.id,
                'cat_id': Cat.id,
                'type': 'subSubCat',
            }
            productArray.append(newrel)

        subCat12 = SubCategory.objects.filter(
            sub_cat_name__contains=inputs['name'])[:2]
        for eachsubcat in subCat12:
            Cat1 = Category.objects.filter(id=eachsubcat.cat_id_id).first()
            newrel = {
                'id': eachsubcat.id,
                'name': eachsubcat.sub_cat_name,
                'brand': Cat1.cat_name,
                'productImage': str(eachsubcat.sub_cat_icon),
                'mrp': '',
                'sellingPrice': '',
                'code': '',
                'cat_id': Cat1.id,
                'type': 'subCat',
            }
            productArray.append(newrel)

        Cat2 = Category.objects.filter(cat_name__contains=inputs['name'])[:2]
        for eachcat in Cat2:
            newrel = {
                'id': eachcat.id,
                'name': eachcat.cat_name,
                'brand': 'Category',
                'productImage': str(eachcat.cat_icon),
                'mrp': '',
                'sellingPrice': '',
                'code': '',
                'type': 'cat',
            }
            productArray.append(newrel)

        return Response(productArray)


class POSAllProductDeleteAPIView(views.APIView):
    def post(self, request):
        newrel = {

        }
        return Response(newrel)


class NotifyMeAPIView(ListCreateAPIView):
    serializer_class = NotifyMeSerializer
    queryset = NotifyMe.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class NotifyMeAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = NotifyMeSerializer
    queryset = NotifyMe.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class LoginOTP(views.APIView):
    def post(self, request):
        inputs = request.data
        template_id = inputs['template_id']
        sms_body = inputs['msg']
        phone_no = inputs['phone_no']
        # smsSend(phone_no, sms_body, template_id)
        # response = requests.get("https://api.datagenit.com/sms?auth=D!~6674T0cAq4CXCS&msisdn=" +
        #                         inputs['phone_no']+"&senderid=QUANTX&message="+inputs['msg']+"&template_id=1207161777825362581")
        # print(response)
        # response = requests.get("http://weberleads.in/http-tokenkeyapi.php?authentic-key=3134696e7374616e745f6765747761793631321586003895&senderid=INGWAY&route=2&number="+inputs['phone_no']+"&message="+inputs['msg'])
        return Response({'sms': 'Otp Send'}, status=status.HTTP_200_OK)


class pincodeSearchAPIView(views.APIView):
    def post(self, request):
        inputs = request.data
        pincode = DeliveryPincode.objects.filter(
            activeStatus=1, pincode__contains=inputs['pincode'])[:10]
        productArray = []
        for eachProd in pincode:
            newrel = {
                'pincode': eachProd.pincode,
            }
            productArray.append(newrel)
        return Response(productArray)


class deliveryHomeAPIView(views.APIView):
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        user_id = self.request.user.id
        pendingDelivery = Booking.objects.filter(Q(orderStatus=1) | Q(
            orderStatus=2) | Q(orderStatus=3), deliveryBoyId=user_id).count()
        completeDelivery = Booking.objects.filter(
            deliveryBoyId=user_id, orderStatus=4).count()
        pendingReturn = Booking.objects.filter(Q(orderStatus=5) | Q(
            orderStatus=6) | Q(orderStatus=7), returnBoyId=user_id).count()
        completeReturn = Booking.objects.filter(
            returnBoyId=user_id, orderStatus=8).count()

        newrel = {
            'pendingDelivery':  pendingDelivery,
            'completeDelivery':  completeDelivery,
            'pendingReturn':  pendingReturn,
            'completeReturn':  completeReturn,
        }
        return Response(newrel)


class SettingsAPIView(ListCreateAPIView):
    serializer_class = SettingsSerializer
    queryset = Settings.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class SettingsAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = SettingsSerializer
    queryset = Settings.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class settingArrayAPIView(views.APIView):
    def post(self, request):
        setting = Settings.objects.first()
        returnArr = {
            'acceptOrder': setting.acceptOrder,
            'appUpdateMandetory': setting.appUpdateMandetory,
            'coupon': setting.coupon,
            'debug': setting.debug,
            'underMantanance': setting.underMantanance,
            'vendorRegistration': setting.vendorRegistration,
            'livePaymentGateway': setting.livePaymentGateway
        }
        return Response(returnArr)


class paymentOptionArr(views.APIView):
    def post(self, request):
        patmentArr = paymentOption.objects.all()
        setting = Settings.objects.first()
        payArr = []
        for eachPayment in patmentArr:
            if setting.livePaymentGateway == True:
                key_secret = eachPayment.live_key_secret
                merchant_Key = eachPayment.live_merchant_Key
            else:
                key_secret = eachPayment.test_key_secret
                merchant_Key = eachPayment.test_merchant_Key
            newArr = {
                'gatwayName': eachPayment.gatewayName,
                'status': eachPayment.status,
                'key_secret': key_secret,
                'merchant_Key': merchant_Key
            }
            payArr.append(newArr)
            # print(key_secret)
        returnArr = {
            'coupon': setting.coupon,
            'acceptOrder': setting.acceptOrder,
            'paymrntOption': payArr
        }
        return Response(returnArr)


class paymentOptionAPIView(ListCreateAPIView):
    serializer_class = paymentOptionSerializer
    queryset = paymentOption.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class paymentOptionAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = paymentOptionSerializer
    queryset = paymentOption.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


def shiprocketLogin():
    url = "https://apiv2.shiprocket.in/v1/external/auth/login"
    payload = json.dumps({
        "email": "",
        "password": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


class AdminGraph(views.APIView):
    def post(self, request):
        bookingDetails = (Booking.objects
                          .annotate(m=Month('OrderDate'))
                          .values('m')
                          #   .values('OrderDate')
                          .annotate(total=Sum('productPayablePrice'))
                          .order_by())
        # for eachBooking in bookingDetails:

        return Response(bookingDetails)


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()
