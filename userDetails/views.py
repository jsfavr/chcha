from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import VendorDetailsSerializer, POSSerializer, UserDetailsSerializer, RewordPointForUserSerializer, MinimumOrderValueForUserSerializer
from rest_framework import permissions, status, views
from .models import VendorDetails, POSDetails, SubscriptionPlan, SubscriptionPlanPurchase, RewordPointForUser, MinimumOrderValueForUser, ReferRewardsList
from wallet.models import Wallet, WalletTransaction
from rest_framework.response import Response
from authentication.models import User
from django.http import HttpResponse
from django.core import serializers
from product.permissions import IsOwner
from django.db.models import Q
from booking.models import Booking, BookingPayment
# Create your views here.
from django.conf import settings
from authentication.utils import Util
from wallet.views import smsSend
from datetime import date


class VendorDetailsAPIView(ListCreateAPIView):
    serializer_class = VendorDetailsSerializer
    queryset = VendorDetails.objects.all()

    def perfrom_create(self, serializer):
        return serializer.save()


class VendorDetailsAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = VendorDetailsSerializer
    queryset = VendorDetails.objects.all()

    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


# Create your views here.
class POSAPIView(ListCreateAPIView):
    serializer_class = POSSerializer
    queryset = POSDetails.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class POSDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = POSSerializer
    queryset = POSDetails.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class VendorResView(views.APIView):
    def post(self, request):
        inputs = request.data
        vendor_details_data = VendorDetails.objects.create(user_id_id=inputs['user_id_id'], aadharNumber=inputs['aadharNumber'], panNumber=inputs['panNumber'], companyName=inputs[
                                                           'companyName'], companyLogo=inputs['companyLogo'], gstNumber=inputs['gstNumber'], aadharImage=inputs['aadharImage'], panImage=inputs['panImage'], vendorSign=inputs['vendorSign'])
        vendor_details_data.save()
        wallet_data = Wallet.objects.create(user_id_id=inputs['user_id_id'])
        wallet_data.save()
        return Response({'vendor_details': 'Successfully Added'}, status=status.HTTP_200_OK)


class UserDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailsSerializer
    queryset = User.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class AllUserDetailsView(views.APIView):
    def get(self, request):
        user_details = User.objects.filter(role_id=1).order_by('-id')
        users = []
        for eachUser in user_details:
            refer = User.objects.filter(referUserID=eachUser.id).count()
            newArr = {
                'id': eachUser.id,
                'name': eachUser.name,
                'email': eachUser.email,
                'phone': eachUser.phone,
                'customerID': eachUser.username,
                'totalRefer': refer,
                'subscriptionType': eachUser.subscriptionStatus,
                'status': eachUser.status
            }
            users.append(newArr)
        return Response(users)


class SearchallUserDetailsView(views.APIView):
    def post(self, request):
        inputs = request.data
        query_string = inputs['search']
        user_details = User.objects.filter(
            Q(username__icontains=query_string) | Q(name__icontains=query_string) | Q(
                phone__icontains=query_string) | Q(email__icontains=query_string),
            role_id=1
        )
        users = []
        for eachUser in user_details:
            refer = User.objects.filter(referUserID=eachUser.id).count()
            newArr = {
                'id': eachUser.id,
                'name': eachUser.name,
                'email': eachUser.email,
                'phone': eachUser.phone,
                'customerID': eachUser.username,
                'totalRefer': refer,
                'subscriptionType': eachUser.subscriptionStatus,
                'status': eachUser.status
            }
            users.append(newArr)
        return Response(users)


class AllVendorUserDetailsView(views.APIView):
    def get(self, request):
        vendor_details = VendorDetails.objects.all()
        modifiedVendor = []
        for eachUser in vendor_details:
            vendor_del = VendorDetails.objects.filter(
                user_id_id=eachUser.user_id_id)
            user_del = User.objects.filter(id=eachUser.user_id_id)
            user_list = serializers.serialize('json', user_del)
            vendor_list = serializers.serialize('json', vendor_del)
            newVendor = {
                'user': user_list,
                'vendor': vendor_list,
            }
            # print(newProd)
            modifiedVendor.append(newVendor)
        # user_list = serializers.serialize('json', user_details)
        # return HttpResponse(user_list, content_type="application/json")
        return Response(modifiedVendor)


class SearchDetailsView(views.APIView):
    def post(self, request):
        inputs = request.data
        query_string = inputs['search']
        vendor = []
        vendor_details = User.objects.filter(
            Q(username__icontains=query_string) | Q(name__icontains=query_string) | Q(
                phone__icontains=query_string) | Q(email__icontains=query_string),
            role_id=2
        )
        if vendor_details:
            for vendor_id in vendor_details:
                vendor.append(vendor_id.id)
        modifiedVendor = []
        for eachUser in vendor:
            # print(eachUser)
            vendor_del = VendorDetails.objects.filter(user_id_id=eachUser)
            if vendor_del:
                user_del = User.objects.filter(id=eachUser)
                user_list = serializers.serialize('json', user_del)
                vendor_list = serializers.serialize('json', vendor_del)
                newVendor = {
                    'user': user_list,
                    'vendor': vendor_list,
                }
                # print(newProd)
                modifiedVendor.append(newVendor)
        # user_list = serializers.serialize('json', user_details)
        # return HttpResponse(user_list, content_type="application/json")
        return Response(modifiedVendor)


class AllDeliveryDetailsView(views.APIView):
    def get(self, request):
        user_details = User.objects.filter(role_id=5)
        user_list = serializers.serialize('json', user_details)
        delivery_boy = {
            'deleiveryboy_details': user_list
        }
        return Response(delivery_boy)


class DeliveryBoyDetailsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id
        user_details = User.objects.filter(id=user_id)
        user_show = []
        for user in user_details:
            name = user.name
            email = user.email
            phone = user.phone

        user_list = {
            'name': name,
            'email': email,
            'phone': phone
        }
        user_show.append(user_list)
        return Response(user_show)


class ReferDetailsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        user_id = self.request.user.id
        referArr = []
        referDetails = User.objects.filter(referUserID=user_id)
        userDetails = User.objects.filter(id=user_id).first()
        for eachRefer in referDetails:
            purchaseDetails = SubscriptionPlanPurchase.objects.filter(
                user_id=eachRefer.id, referUserID=user_id).first()
            if purchaseDetails:
                statusVideo = purchaseDetails.videoStatus
                purchaseid = purchaseDetails.id
            else:
                statusVideo = False
                purchaseid = 0

            newarr = {
                'id': eachRefer.id,
                'email': eachRefer.email,
                'name': eachRefer.name,
                'phone': eachRefer.phone,
                'subscriptionStatus': eachRefer.subscriptionStatus,
                'register_date': eachRefer.created_at,
                'videoStatus': statusVideo,
                'purchaseList_id': purchaseid


            }
            referArr.append(newarr)
        planDetails = SubscriptionPlan.objects.first()
        returnArr = {
            'subscriptionStatus': userDetails.subscriptionStatus,
            'subscriptionPrice': planDetails.price,
            'referCode': self.request.user.username,
            'referArr': referArr
        }
        return Response(returnArr)


class RewardsListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        user_id = self.request.user.id
        referArr = []
        referDetails = ReferRewardsList.objects.filter(
            user_id=user_id).order_by('-id')
        for eachRefer in referDetails:
            userDetails = User.objects.filter(
                id=eachRefer.register_user_id).first()

            newarr = {
                'email': userDetails.email,
                'name': userDetails.name,
                'phone': userDetails.phone,
                'amount': eachRefer.amount,
                'level': eachRefer.cashbackLevel,
                'register_date': userDetails.created_at,
                'rewardsList_id': eachRefer.id,
                'cashbackStatus': eachRefer.cashbackStatus
            }
            referArr.append(newarr)
        planDetails = SubscriptionPlan.objects.first()
        returnArr = {
            'subscriptionStatus': self.request.user.subscriptionStatus,
            'subscriptionPrice': planDetails.price,
            'referCode': self.request.user.username,
            'referArr': referArr
        }
        return Response(returnArr)


class UserDetails(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        user_id = self.request.user.id
        subsDetails = SubscriptionPlanPurchase.objects.filter(
            user_id_id=user_id).first()
        if subsDetails:
            userArr = {
                'name': self.request.user.name,
                'email': self.request.user.email,
                'phone': self.request.user.phone,
                'referCode': self.request.user.username,
                'subscriptionStatus': self.request.user.subscriptionStatus,
                'subscriptionPrice': subsDetails.price,
                'orderID': subsDetails.orderID,
                'transID': subsDetails.transID,

            }
        else:
            planDetails = SubscriptionPlan.objects.first()
            userArr = {
                'name': self.request.user.name,
                'email': self.request.user.email,
                'phone': self.request.user.phone,
                'referCode': self.request.user.username,
                'subscriptionStatus': self.request.user.subscriptionStatus,
                'subscriptionPrice': planDetails.price,
                'orderID': 0,
                'transID': 0
            }
        return Response(userArr)


class subscribe(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        user_id = self.request.user.id
        inputs = request.data

        userDetails = User.objects.filter(id=user_id).first()
        referUserDetails = User.objects.filter(
            id=userDetails.referUserID).first()
        referCashback = 100
        referUserID = 0
        if referUserDetails:
            referUserID = userDetails.referUserID
            addRewardToDB(user_id, user_id, 6)
            # referWalletBalance = Wallet.objects.filter(
            #     user_id_id=userDetails.referUserID).first()
            # WalletTransaction.objects.create(
            #     transactionAmount=referCashback,
            #     afterTransactionAmount=referWalletBalance.amount+referCashback,
            #     remarks='Refer Cashback',
            #     transactionType='CREDIT',
            #     user_id_id=userDetails.referUserID
            # )
            # if referWalletBalance :
            #     Wallet.objects.filter(user_id_id=userDetails.referUserID).update(
            #         amount=referWalletBalance.amount+referCashback
            #     )
            # else:
            #     Wallet.objects.create(
            #         user_id_id=userDetails.referUserID,
            #         amount=referWalletBalance.amount+referCashback
            #     )

        SubscriptionPlanPurchase.objects.create(
            price=inputs['price'],
            user_id_id=user_id,
            orderID=inputs['orderID'],
            transID=inputs['transID'],
            referUserID=referUserID
        )
        User.objects.filter(id=user_id).update(
            subscriptionStatus=True
        )
        walletBalance = Wallet.objects.filter(user_id_id=user_id).first()
        if walletBalance:
            Wallet.objects.filter(user_id_id=user_id).update(
                point=int(walletBalance.point)+int(inputs['price']),
                totalPoint=int(walletBalance.totalPoint)+int(inputs['price'])
            )
        else:
            Wallet.objects.create(
                user_id_id=user_id,
                point=int(walletBalance.point)+int(inputs['price']),
                totalPoint=int(walletBalance.totalPoint)+int(inputs['price'])
            )
        WalletTransaction.objects.create(
            transactionAmount=inputs['price'],
            afterTransactionAmount=int(
                walletBalance.point)+int(inputs['price']),
            remarks='Power Purchase',
            transactionType='CREDIT',
            user_id_id=user_id,
            walletType='REWARDS'
        )

        today = date.today()
        template_id = ''
        sms_body = 'Hi '+str(self.request.user.name)+', You entire in Crowd Power member effective from ' + \
            str(today.strftime("%B %d, %Y")) + \
            ' enjoy all the best e-commerce & training program.'
        phone_no = self.request.user.phone
        name = self.request.user.name
        email = self.request.user.email
        smsSend(phone_no, sms_body, template_id)
        data = {
            'name': name,
            'email': email,
            'subject': 'Power Successfully',
            'message': 'You entire in Crowd Power member effective from ' + str(today.strftime("%B %d, %Y")) + ' enjoy all the best e-commerce & training program.',
            'from_email': settings.EMAIL_HOST_USER
        }
        Util.email_send(data)
        newArr = {
            'msg': 'subscription Successfully',
            'status': True
        }
        return Response(newArr)


class subscribeFromAdmin(views.APIView):
    def post(self, request):
        inputs = request.data
        user_id = inputs['user_id']
        userDetails = User.objects.filter(id=user_id).first()
        referUserDetails = User.objects.filter(
            id=userDetails.referUserID).first()
        referCashback = 100
        referUserID = 0
        if referUserDetails:
            referUserID = userDetails.referUserID
            addRewardToDB(user_id, user_id, 6)
            # referWalletBalance = Wallet.objects.filter(
            #     user_id_id=userDetails.referUserID).first()
            # WalletTransaction.objects.create(
            #     transactionAmount=referCashback,
            #     afterTransactionAmount=referWalletBalance.amount+referCashback,
            #     remarks='Refer Cashback',
            #     transactionType='CREDIT',
            #     user_id_id=userDetails.referUserID
            # )
            # if referWalletBalance :
            #     Wallet.objects.filter(user_id_id=userDetails.referUserID).update(
            #         amount=referWalletBalance.amount+referCashback
            #     )
            # else:
            #     Wallet.objects.create(
            #         user_id_id=userDetails.referUserID,
            #         amount=referWalletBalance.amount+referCashback
            #     )
        subcrPrice = SubscriptionPlan.objects.first()
        SubscriptionPlanPurchase.objects.create(
            price=subcrPrice.price,
            user_id_id=user_id,
            orderID=inputs['orderID'],
            transID=inputs['transID'],
            referUserID=referUserID
        )
        User.objects.filter(id=user_id).update(
            subscriptionStatus=True
        )
        walletBalance = Wallet.objects.filter(user_id_id=user_id).first()
        if walletBalance:
            Wallet.objects.filter(user_id_id=user_id).update(
                point=int(walletBalance.point)+int(subcrPrice.price),
                totalPoint=int(walletBalance.totalPoint)+int(subcrPrice.price)
            )
        else:
            Wallet.objects.create(
                user_id_id=user_id,
                point=int(walletBalance.point)+int(subcrPrice.price),
                totalPoint=int(walletBalance.totalPoint)+int(subcrPrice.price)
            )
        WalletTransaction.objects.create(
            transactionAmount=subcrPrice.price,
            afterTransactionAmount=int(
                walletBalance.point)+int(subcrPrice.price),
            remarks='Power Purchase',
            transactionType='CREDIT',
            user_id_id=user_id,
            walletType='REWARDS'
        )

        today = date.today()
        template_id = ''
        userDetails = User.objects.filter(id=user_id).first()
        sms_body = 'Hi '+str(userDetails.name)+', You entire in Crowd Power member effective from ' + \
            str(today.strftime("%B %d, %Y")) + \
            ' enjoy all the best e-commerce & training program.'
        phone_no = userDetails.phone
        name = userDetails.name
        email = userDetails.email
        smsSend(phone_no, sms_body, template_id)
        data = {
            'name': name,
            'email': email,
            'subject': 'Power Successfully',
            'message': 'You entire in Crowd Power member effective from ' + str(today.strftime("%B %d, %Y")) + ' enjoy all the best e-commerce & training program.',
            'from_email': settings.EMAIL_HOST_USER
        }
        Util.email_send(data)
        newArr = {
            'msg': 'subscription Successfully',
            'status': True
        }
        return Response(newArr)


class UserDetailsAdmin(views.APIView):
    def get(self, request, id):
        userDetails = User.objects.filter(id=id).first()
        perchaseDetails = SubscriptionPlanPurchase.objects.filter(
            user_id_id=id).first()
        walletDetails = Wallet.objects.filter(user_id_id=id).first()
        if perchaseDetails:
            price = perchaseDetails.price
            orderID = perchaseDetails.orderID
            transID = perchaseDetails.transID
            created_at = perchaseDetails.created_at
        else:
            price = ''
            orderID = ''
            transID = ''
            created_at = ''
        if userDetails.referUserID != 0:
            referDetails = User.objects.filter(
                id=userDetails.referUserID).first()
            referrerArr = {
                'id': referDetails.id,
                'name': referDetails.name,
                'email': referDetails.email,
                'phone': referDetails.phone,
                'referCode': referDetails.username
            }
        else:
            referrerArr = {
                'id': 0,
                'name': 0,
                'email': 0,
                'phone': 0,
                'referCode': 0
            }

        userArr = {
            'id': userDetails.id,
            'name': userDetails.name,
            'email': userDetails.email,
            'phone': userDetails.phone,
            'referCode': userDetails.username,
            'CustomersID': userDetails.username,
            'referrerCode': userDetails.refer_code,
            'subscriptionStatus': userDetails.subscriptionStatus,
            'price': price,
            'orderID': orderID,
            'transID': transID,
            'created_at': created_at,
            'walletBalance': walletDetails.amount,
            'walletPoint': walletDetails.point,


        }
        walletTrans = WalletTransaction.objects.filter(
            user_id_id=id).order_by('-id')[:10]
        walletArr = []
        for eachWalletTrans in walletTrans:
            newArr = {
                'transactionAmount': eachWalletTrans.transactionAmount,
                'afterTransactionAmount': eachWalletTrans.afterTransactionAmount,
                'remarks': eachWalletTrans.remarks,
                'transactionType': eachWalletTrans.transactionType,
                'walletType': eachWalletTrans.walletType,
                'updated_at': eachWalletTrans.updated_at
            }
            walletArr.append(newArr)
        referArr = []
        referDetails = User.objects.filter(referUserID=id).order_by('-id')
        for eachReferDetails in referDetails:
            purchaseDetails = SubscriptionPlanPurchase.objects.filter(
                user_id_id=eachReferDetails.id).first()
            refer = User.objects.filter(
                referUserID=eachReferDetails.id).count()
            subscription_date = ''
            if purchaseDetails:
                subscription_date = purchaseDetails.created_at
            arr = {
                'user_id': eachReferDetails.id,
                'user_name': eachReferDetails.name,
                'user_email': eachReferDetails.email,
                'user_phone': eachReferDetails.phone,
                'register_date': eachReferDetails.created_at,
                'subscription_status': eachReferDetails.subscriptionStatus,
                'subscription_date': subscription_date,
                'totalRefer': refer
            }
            referArr.append(arr)

        booking_history = BookingPayment.objects.filter(
            user_id_id=id).order_by('-id')
        booking_array = []
        for book in booking_history:
            booking_payment = {
                'grandTotal': book.grandTotal,
                'paymentType': book.paymentType,
                'deliveryCharge': book.deliveryCharge,
                'walletAmount': book.walletAmount,
                'couponDiscount': book.couponDiscount
            }
            bookings = Booking.objects.filter(bookingPaymentID=book.id)
            order_id = []
            for bk in bookings:
                booking_details = {
                    'OrderID': bk.orderID,
                    'booking_id': bk.id,
                    'date': bk.OrderDate
                }
                order_id.append(booking_details)
            users = User.objects.filter(id=book.user_id_id)
            for user in users:
                uname = user.name
                uphone = user.phone
                uemail = user.email
                uid = user.id
            UserDetails = {
                'id': uid,
                'name': uname,
                'phone': uphone,
                'email': uemail
            }
            details = {
                'bookingPayment': booking_payment,
                'orderId': order_id,
                'userDetails': UserDetails,

            }
            booking_array.append(details)
        returnArr = {
            'userArr': userArr,
            'walletArr': walletArr,
            'referArr': referArr,
            'bookingArr': booking_array,
            'referrerArr': referrerArr
        }
        return Response(returnArr)


class GetPlan(views.APIView):
    def get(self, request):
        plan = SubscriptionPlan.objects.first()
        newArr = {
            'price': plan.price
        }
        return Response(newArr)


class PurchaseList(views.APIView):
    def get(self, request):
        purchase = SubscriptionPlanPurchase.objects.order_by('-id')
        purchaseArr = []
        for eachPurchase in purchase:
            userDetails = User.objects.filter(
                id=eachPurchase.user_id_id).first()
            newArr = {
                'user_id': userDetails.id,
                'user_name': userDetails.name,
                'user_email': userDetails.email,
                'user_phone': userDetails.phone,
                'price': eachPurchase.price,
                'transID': eachPurchase.transID,
                'OrderID': eachPurchase.orderID,
                'date': eachPurchase.created_at
            }
            purchaseArr.append(newArr)
        return Response(purchaseArr)


class sendCashBack(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = inputs['id']
        purchaseDetails = SubscriptionPlanPurchase.objects.filter(
            user_id=user_id, referUserID=self.request.user.id).first()
        if purchaseDetails.videoStatus:
            newArr = {
                'msg': 'Point already send',
                'status': True
            }
        else:
            sendReward(user_id, 6)
            SubscriptionPlanPurchase.objects.filter(
                user_id=user_id, referUserID=self.request.user.id).update(videoStatus=True)
            newArr = {
                'msg': 'Point send Successfully',
                'status': True
            }
        return Response(newArr)


class sendCashBackNew(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        purchaseDetails = ReferRewardsList.objects.filter(
            id=inputs['rewardsList_id']).first()
        if purchaseDetails.cashbackStatus:
            newArr = {
                'msg': 'Point already send',
                'status': True
            }
        else:
            referCashback = purchaseDetails.amount
            referWalletBalance = Wallet.objects.filter(
                user_id_id=purchaseDetails.user_id).first()
            if referWalletBalance:
                Wallet.objects.filter(user_id_id=purchaseDetails.user_id).update(
                    point=referWalletBalance.point+referCashback
                )
            else:
                Wallet.objects.create(
                    user_id_id=purchaseDetails.user_id,
                    point=referWalletBalance.point+referCashback,
                    totalPoint=int(
                        referWalletBalance.totalPoint)+int(referCashback)
                )
            if purchaseDetails.cashbackLevel == 1:
                st = 'st'
            elif purchaseDetails.cashbackLevel == 2:
                st = 'nd'
            elif purchaseDetails.cashbackLevel == 3:
                st = 'rd'
            else:
                st = 'th'
            WalletTransaction.objects.create(
                transactionAmount=referCashback,
                afterTransactionAmount=referWalletBalance.point+referCashback,
                remarks='Referral Rewards',
                transactionType='CREDIT',
                user_id_id=purchaseDetails.user_id,
                walletType='REWARDS'
            )
            ReferRewardsList.objects.filter(
                id=inputs['rewardsList_id']).update(cashbackStatus=True)
            newArr = {
                'msg': 'Point send Successfully',
                'status': True
            }
        return Response(newArr)


def sendReward(user_id, level):
    rewardsArr = [10, 20, 30, 40, 50, 100]
    if level > 0:
        userDetails = User.objects.filter(id=user_id).first()
        referUserDetails = User.objects.filter(
            id=userDetails.referUserID).first()
        referCashback = rewardsArr[level-1]
        if referUserDetails:
            print("level - "+str(7-level)+" register_user_id - " +
                  str(user_id) + " refer_user_id - "+str(userDetails.referUserID) + " rewards - "+str(referCashback))
            referWalletBalance = Wallet.objects.filter(
                user_id_id=userDetails.referUserID).first()
            if referWalletBalance:
                Wallet.objects.filter(user_id_id=userDetails.referUserID).update(
                    point=referWalletBalance.point+referCashback
                )
            else:
                Wallet.objects.create(
                    user_id_id=userDetails.referUserID,
                    point=referWalletBalance.point+referCashback,
                    totalPoint=int(
                        referWalletBalance.totalPoint)+int(referCashback)
                )
            WalletTransaction.objects.create(
                transactionAmount=referCashback,
                afterTransactionAmount=referWalletBalance.point+referCashback,
                remarks='Referral Rewards',
                transactionType='CREDIT',
                user_id_id=userDetails.referUserID,
                walletType='REWARDS'
            )
            sendReward(userDetails.referUserID, int(level-1))
        else:
            print('not found')


def addRewardToDB(register_user_id, user_id, level):
    rewardsArr = [10, 20, 30, 40, 50, 100]
    if level > 0:
        userDetails = User.objects.filter(id=user_id).first()
        referUserDetails = User.objects.filter(
            id=userDetails.referUserID).first()
        referCashback = rewardsArr[level-1]
        if referUserDetails:
            print("level - "+str(7-level)+" register_user_id - " +
                  str(user_id) + " refer_user_id - "+str(userDetails.referUserID) + " rewards - "+str(referCashback))
            # Rewards add to db
            parentDetails = User.objects.filter(
                id=userDetails.referUserID).first()
            if parentDetails.referUserID:
                parent_user_id = parentDetails.referUserID
            else:
                parent_user_id = 0
            ReferRewardsList.objects.create(
                user_id=userDetails.referUserID,
                register_user_id=register_user_id,
                parent_user_id=parent_user_id,
                cashbackLevel=int(7-level),
                amount=referCashback
            )

            # referWalletBalance = Wallet.objects.filter(
            #     user_id_id=userDetails.referUserID).first()
            # if referWalletBalance:
            #     Wallet.objects.filter(user_id_id=userDetails.referUserID).update(
            #         point=referWalletBalance.point+referCashback
            #     )
            # else:
            #     Wallet.objects.create(
            #         user_id_id=userDetails.referUserID,
            #         point=referWalletBalance.point+referCashback,
            #         totalPoint=int(
            #             referWalletBalance.totalPoint)+int(referCashback)
            #     )
            # WalletTransaction.objects.create(
            #     transactionAmount=referCashback,
            #     afterTransactionAmount=referWalletBalance.point+referCashback,
            #     remarks='Referral Rewards',
            #     transactionType='CREDIT',
            #     user_id_id=userDetails.referUserID,
            #     walletType='REWARDS'
            # )
            addRewardToDB(register_user_id,
                          userDetails.referUserID, int(level-1))
        else:
            print('not found')
# Create your views here.


class RewordPointForUserAPIView(ListCreateAPIView):
    serializer_class = RewordPointForUserSerializer
    queryset = RewordPointForUser.objects.all()

    def perfrom_create(self, serializer):
        return serializer.save()


class RewordPointForUserAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = RewordPointForUserSerializer
    queryset = RewordPointForUser.objects.all()

    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


# Create your views here.
class MinimumOrderValueForUserAPIView(ListCreateAPIView):
    serializer_class = MinimumOrderValueForUserSerializer
    queryset = MinimumOrderValueForUser.objects.all()

    def perfrom_create(self, serializer):
        return serializer.save()


class MinimumOrderValueForUserAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = MinimumOrderValueForUserSerializer
    queryset = MinimumOrderValueForUser.objects.all()

    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class CheckUser(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        user_id = self.request.user.id
        UserDetails = User.objects.filter(id=user_id).first()
        if UserDetails:
            if UserDetails.status == True:
                returnArr = {
                    'status': 1,
                    'msg': 'User Status True'
                }
            else:
                returnArr = {
                    'status': 2,
                    'msg': 'User Blocked'
                }
        else:
            returnArr = {
                'status': 3,
                'msg': 'User Not Found'
            }
        return Response(returnArr)
