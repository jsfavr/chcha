from django.shortcuts import render
from rest_framework import permissions, views, status
from product.permissions import IsOwner
from django.core import serializers
from rest_framework.response import Response
from cart.models import NonCart, Cart
from product.models import Product, ProductBrand
from userDetails.models import VendorDetails
from category.models import SubCategory
from wallet.models import Wallet, WalletTransaction
from address.models import ShippingAddress, DeliveryPincode
from banner.models import Coupon
from authentication.models import User
from booking.models import Booking, BookingPayment
from category.models import SubCategory
from other.models import InventoryTransaction
from django.conf import settings
from authentication.utils import Util
import razorpay
import requests
from other.models import paymentOption, Settings
from userDetails.models import RewordPointForUser, MinimumOrderValueForUser
from wallet.views import smsSend
import math
# Create your views here.


class checkoutItemsAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        if inputs['product_id'] != "0":
            NonCart.objects.filter(user_id_id=user_id).delete()
            NonCart.objects.create(
                product_id_id=inputs['product_id'], user_id_id=user_id, quantity=inputs['qty'])
            items = NonCart.objects.filter(user_id_id=user_id)
        else:
            items = Cart.objects.filter(user_id_id=user_id)

        modifiedProduct = []
        cartTotal = 0
        wallet_amount = 0
        gst1 = 0
        for eachrel in items:
            product = Product.objects.filter(id=eachrel.product_id_id)
            for eachProd1 in product:
                vendor = VendorDetails.objects.filter(
                    user_id_id=eachProd1.user_id_id)
                for eachvendor in vendor:
                    companyName = eachvendor.companyName

                subcatdel = SubCategory.objects.filter(
                    id=eachProd1.sub_cat_id_id)
                for eachsubcatdel in subcatdel:
                    price = eachProd1.sellingPrice + \
                        (eachProd1.sellingPrice*eachsubcatdel.gst)/100
                    gst = (eachProd1.sellingPrice *
                           eachsubcatdel.gst)/100

                brand = ProductBrand.objects.filter(
                    id=eachProd1.productBrandID_id)
                for eachbrand in brand:
                    brandName = eachbrand.brand_name

                pro = {
                    'id': eachProd1.id,
                    'name': eachProd1.productName,
                    'brand': brandName,
                    'mrp': eachProd1.mrp,
                    'copmany_name': companyName,
                    'selling_price': round(price),
                    'order_qty': eachrel.quantity,
                    'order_value': round(price)*eachrel.quantity,
                }
            modifiedProduct.append(pro)
            cartTotal = cartTotal+round(price)*eachrel.quantity
            print(gst)
            gst1 = gst1+(gst*eachrel.quantity)

        wallets = Wallet.objects.filter(user_id_id=user_id)
        for eachwallet in wallets:
            wallet_amount = eachwallet.amount
            wallet_point = eachwallet.point

        walletPointPercentage = RewordPointForUser.objects.first()
        percentageValue = (wallet_point*walletPointPercentage.percentage)/100
        minimumOrderValue = MinimumOrderValueForUser.objects.first()
        response = {
            'cart_total': cartTotal,
            'product': modifiedProduct,
            'wallet_amount': wallet_amount,
            'wallet_point': wallet_point,
            'maximumUsewalletPoint': round(percentageValue),
            'maximumOrderValue': round(minimumOrderValue.value),
            'totalGST': gst1
        }
        return Response(response)


class findDeliveryChargeAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        ship = ShippingAddress.objects.filter(id=inputs['address_id']).first()
        pincode = ship.pincode
        if pincode: 
            delivery = DeliveryPincode.objects.filter(
                pincode=pincode, activeStatus=1)
            if len(delivery) > 0:
                for eachdelivery in delivery:
                    if eachdelivery.minPrice < inputs['payble_amount']:
                        deliveryCharge = 0
                    else:
                        deliveryCharge = eachdelivery.deliveryCharge

                    details = {
                        'pincode': eachdelivery.pincode,
                        'payble_amount': inputs['payble_amount'],
                        'delivery_charge': deliveryCharge,
                        'cod': eachdelivery.cod
                    }
                    status = {
                        'msg': 'Pincode Serviceable',
                        'code': 1,
                    }
            else:
                details = {
                    'pincode': '',
                    'payble_amount': inputs['payble_amount'],
                    'delivery_charge': 0,
                }
                status = {
                    'msg': 'Pincode not Serviceable',
                    'code': 1,
                }

            response = {
                'status': status,
                'details': details, 
            }
            
            return Response(response)
        else:
            return Response({'msg':'Address colud not find'},status=status.HTTP_400_BAD_REQUEST)



class findCouponAvailabilityAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        details = []
        coupon = Coupon.objects.filter(couponCode=inputs['couponCode'])
        if len(coupon) > 0:
            coupon1 = Coupon.objects.filter(
                couponCode=inputs['couponCode'], activeStatus=1)
            if len(coupon1) > 0:
                coupon12 = BookingPayment.objects.filter(
                    couponCode=inputs['couponCode'], user_id=user_id)
                if len(coupon12) == 0:
                    couponDetails = Coupon.objects.filter(
                        couponCode=inputs['couponCode'])
                    for couponDetails1 in couponDetails:
                        if couponDetails1.minPrice <= (inputs['payble_amount']-inputs['total_gst']):
                            status = {
                                'msg': 'Coupon Code applied',
                                'code': 4,
                            }
                            if couponDetails1.couponType == 'PERSENTAGE':
                                details = {
                                    'discount_value': (((inputs['payble_amount']-inputs['total_gst'])*couponDetails1.discount)/100),
                                    'discount_payble_value': (inputs['payble_amount']-((inputs['payble_amount']*couponDetails1.discount)/100)),
                                }
                            else:
                                details = {
                                    'discount_value': couponDetails1.discount,
                                    'discount_payble_value': inputs['payble_amount']-couponDetails1.discount,
                                }
                        else:
                            status = {
                                'msg': 'Payable Amount must be Grater then '+str(couponDetails1.minPrice)+' rupees',
                                'code': 3,
                            }
                else:
                    status = {
                        'msg': 'Coupon Code already used',
                        'code': 2,
                    }
            else:
                status = {
                    'msg': 'Coupon Code Expair',
                    'code': 1,
                }
        else:
            status = {
                'msg': 'Invalid Coupon Code',
                'code': 0,
            }
        response = {
            'status': status,
            'details': details,

        }
        return Response(response)


class paymentCaptureAPIView(views.APIView):
    def post(self, request):
        inputs = request.data
        setting = Settings.objects.first()
        patmentArr = paymentOption.objects.filter(
            gatewayName='Razorpay').first()
        if setting.livePaymentGateway == True:
            merchant_Key = patmentArr.live_merchant_Key
            key_secret = patmentArr.live_key_secret
        else:
            key_secret = patmentArr.test_key_secret
            merchant_Key = patmentArr.test_merchant_Key
        client = razorpay.Client(
            auth=(key_secret, merchant_Key))

        DATA = {
            'amount': inputs['amt_val'],
            'currency': 'INR',
            'receipt': inputs['order_id']
        }
        res = client.order.create(data=DATA)
        return Response(res)


class orderSubmitAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        user_details = User.objects.filter(id=user_id).first()
        phone_no = self.request.user.phone
        email = self.request.user.email
        name = self.request.user.name
        grand_total = int(inputs['total_payble_value'])
        sub_total = int(inputs['cart_total'])
        address_id = inputs['address_id']
        razorpay_payment_id = inputs['razorpay_payment_id']
        payment_type = inputs['payment_type']
        delivery_charge = int(inputs['shipping_charge'])
        coupon_discount = int(inputs['coupon_discount'])
        coupon_code = ''
        if(inputs['coupon_code']):
            coupon_code = inputs['coupon_code']
            
        productList = Cart.objects.filter(user_id_id=user_id)
        if len(productList) != 0:
            booking_payment = BookingPayment.objects.create(
                grandTotal=grand_total,
                subTotal=sub_total,
                razorpayPaymentId=razorpay_payment_id,
                paymentType=payment_type,
                deliveryCharge=delivery_charge,
                walletAmount=0,
                walletPoint=0,
                couponDiscount=coupon_discount,
                couponCode=coupon_code,
                shippingAddressId_id=address_id,
                user_id_id=user_id
            )
            booking_payment.save()
            booking_payment_id = booking_payment.id
            for productLists in productList:
                product = Product.objects.filter(
                    id=productLists.product_id_id)

                for eachProduct in product:
                    perProductSellingPrice = eachProduct.sellingPrice
                    availableStock = eachProduct.availableStock
                    orderCount = eachProduct.orderCount
                    sub_cat = SubCategory.objects.filter(
                        id=eachProduct.sub_cat_id_id)
                    for eachsub_cat in sub_cat:
                        gstPercentage = eachsub_cat.gst

                gstValue = (
                    (perProductSellingPrice*gstPercentage)/100)
            
                ORDER_ID = inputs['order_id']      

                Booking.objects.create(
                    product_id_id=productLists.product_id_id,
                    quantity=productLists.quantity,
                    productSellingPrice=perProductSellingPrice,
                    productGST=gstValue,
                    productPayablePrice=(round(
                        perProductSellingPrice+gstValue)*productLists.quantity),
                    orderID=ORDER_ID,
                    deliveryCharge=delivery_charge,
                    walletAmount=0,
                    walletPoint=0,
                    couponDiscount=coupon_discount,
                    couponCode=coupon_code,
                    paymentType=payment_type,
                    razorpayPaymentId=razorpay_payment_id,
                    shippingAddressId_id=address_id,
                    bookingPaymentID_id=booking_payment_id,
                    user_id_id=user_id
                )
                Product.objects.filter(id=productLists.product_id_id).update(
                    availableStock=availableStock-productLists.quantity, orderCount=orderCount+1)
                InventoryTransaction.objects.create(product_id_id=productLists.product_id_id, quantity=productLists.quantity, remarks='Booking',
                                                    transactionType='DEBIT', transactionID=ORDER_ID, afterTransactionQuantity=availableStock-productLists.quantity)

           
            productList = Cart.objects.filter(
                user_id_id=user_id).delete()

            newrel = {
                'status': 'Booking Successfull',
                'code': 1,
            }
        else:
            newrel = {
                'status': 'No item found',
                'code': 2,
            }
            sms_body = 'Booking Successful : Thank you for ordering with Crowd, Your order is successfully placed. We will notify you as soon as when your order is ready.'

            # data = {
            #     'name': name,
            #     'email': email,
            #     'subject': 'Order Placed Successfully',
            #     'message': 'Thank you for ordering with Crowd, Your order is successfully placed. We will notify you as soon as when your order is ready.',
            #     'from_email': settings.EMAIL_HOST_USER
            # }
            # Util.email_send(data)

            # template_id = '1207161779674247058'
            # smsSend(phone_no, sms_body, template_id)
        
        return Response(newrel)
