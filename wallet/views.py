from django.shortcuts import render
from rest_framework import response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import BankDetailsSerializer, WalletSerializer, WalletTransactionSerializer, WalletWithdrawSerializer
from rest_framework import permissions, views, status
from .models import WalletWithdraw, WalletTransaction, Wallet, BankDetails
from product.permissions import IsOwner
from django.core import serializers
from rest_framework.response import Response
from booking.models import Booking
from authentication.models import User
import requests
from django.conf import settings
from .utils import Util
# Create your views here.


class WalletWithdrawAPIView(ListCreateAPIView):
    serializer_class = WalletWithdrawSerializer
    queryset = WalletWithdraw.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class WalletWithdrawDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = WalletWithdrawSerializer
    queryset = WalletWithdraw.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class WalletTransactionAPIView(ListCreateAPIView):
    serializer_class = WalletTransactionSerializer
    queryset = WalletTransaction.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class WalletTransactionDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = WalletTransactionSerializer
    queryset = WalletTransaction.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class WalletAPIView(ListCreateAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class WalletDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class BankDetailsAPIView(ListCreateAPIView):
    serializer_class = BankDetailsSerializer
    queryset = BankDetails.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class BankDetailsDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BankDetailsSerializer
    queryset = BankDetails.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class WalletGetAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id
        data = Wallet.objects.filter(user_id_id=user_id)
        wallet_details = serializers.serialize('json', data)
        return Response(wallet_details)


class WalletTransectionGetAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id
        data = WalletTransaction.objects.filter(
            user_id_id=user_id).order_by('-id')[:10]
        wallet_transaction_details = serializers.serialize('json', data)
        return Response(wallet_transaction_details)


class WalletBankGetAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id
        print(user_id)
        user_details = BankDetails.objects.filter(user_id_id=user_id).first()

        user_list = []
        # for user in user_details:
        #     id=user.id
        #     bank=user.bankName
        #     account=user.AccountNumber
        #     name=user.accountHolderName
        #     ifsc=user.ifscCode
        #     branch=user.branchName
        #     upi=user.upi
        if user_details:
            user_list = {
                'id': user_details.id,
                'bank': user_details.bankName,
                'account': user_details.AccountNumber,
                'name': user_details.accountHolderName,
                'ifsc': user_details.ifscCode,
                'branch': user_details.branchName,
                'upi': user_details.upi
            }
        # user_show.append(user_list)
        return Response(user_list)


class WalletWithdrawGetAPI(views.APIView):
    def post(self, request):
        inputs = request.data
        reddemPrice = 10
        status = inputs['order_status']
        if status == 4:
            wallet = Wallet.objects.filter(user_id_id=inputs['user_id'])
            for eachWallet in wallet:
                # print(eachWallet)
                currentBalance = eachWallet.amount
                # print(currentBalance)

                updatedWalletBalance = currentBalance+reddemPrice

            walletUpdate = Wallet.objects.filter(
                user_id_id=inputs['user_id']).update(amount=updatedWalletBalance)
            WalletTransCreate = WalletTransaction.objects.create(
                user_id_id=inputs['user_id'], transactionAmount=reddemPrice, afterTransactionAmount=updatedWalletBalance, remarks='Order Returned', transactionType='CREDIT')
        else:
            wallet = Wallet.objects.filter(user_id_id=inputs['user_id'])
            for eachWallet in wallet:
                # print(eachWallet)
                currentBalance = eachWallet.amount
                # print(currentBalance)

                updatedWalletBalance = currentBalance+reddemPrice

            walletUpdate = Wallet.objects.filter(
                user_id_id=inputs['user_id']).update(amount=updatedWalletBalance)
            WalletTransCreate = WalletTransaction.objects.create(
                user_id_id=inputs['user_id'], transactionAmount=reddemPrice, afterTransactionAmount=updatedWalletBalance, remarks='Order Return', transactionType='CREDIT')
        return Response({'status': 'Wallet  Add'})


class vendorWithdrawRequest(views.APIView):
    def get(self, request):
        arr = []
        withdraw = WalletWithdraw.objects.all().order_by('-id')
        for eachwithdraw in withdraw:
            withdrawAmount = eachwithdraw.amount
            date = eachwithdraw.updated_at
            id = eachwithdraw.id
            status = eachwithdraw.status
            transID = eachwithdraw.transID

            vendor = User.objects.filter(id=eachwithdraw.user_id_id).first()
            name = vendor.name
            phone = vendor.phone
            email = vendor.email

            wallet = Wallet.objects.filter(user_id_id=eachwithdraw.user_id_id)
            for eachwallet in wallet:
                walletAmount = eachwallet.amount

            bank = BankDetails.objects.filter(
                user_id_id=eachwithdraw.user_id_id)
            if bank:
                for eachbank in bank:
                    print(eachbank.bankName)
                    acc_no = eachbank.AccountNumber
                    ifsc = eachbank.ifscCode
                    bank = eachbank.bankName
                    accHolder = eachbank.accountHolderName
                    branchName = eachbank.branchName
                    upi = eachbank.upi
            else:
                acc_no = ''
                ifsc = ''
                bank = ''
                accHolder = ''
                branchName = ''
                upi = ''

            user_list = {
                'id': id,
                'status': status,
                'transID': transID,
                'bank': bank,
                'account': acc_no,
                'name': accHolder,
                'ifsc': ifsc,
                'branch': branchName,
                'upi': upi,
                'vendorName': name,
                'phone': phone,
                'email': email,
                'date': date,
                'walletAmount': walletAmount,
                'withdrawAmount': withdrawAmount,
                'user_id': vendor.id
            }
            arr.append(user_list)
        return Response(arr)


class vendorPayment(views.APIView):
    def post(self, request):
        inputs = request.data
        withDraw = WalletWithdraw.objects.filter(
            id=inputs['withdraw_id']).first()
        if withDraw:
            userId = withDraw.user_id_id
            wallet = Wallet.objects.filter(user_id_id=userId).first()
            currentBalance = wallet.amount
            reddemPrice = withDraw.amount
            updatedWalletBalance = currentBalance-reddemPrice
            if currentBalance >= reddemPrice:
                Wallet.objects.filter(user_id_id=userId).update(
                    amount=updatedWalletBalance)
                WalletTransaction.objects.create(user_id_id=userId, transactionAmount=reddemPrice,
                                                 afterTransactionAmount=updatedWalletBalance, remarks='Withdraw of '+str(reddemPrice), transactionType='DEBIT')
                WalletWithdraw.objects.filter(id=inputs['withdraw_id']).update(
                    status=1, transID=inputs['transID'])
                userDetails = User.objects.filter(id=userId).first()
                phone = userDetails.phone
                email = userDetails.email
                name = userDetails.name
                message = 'Dear Customer, Your Wallet balance withdrawal request of ' + \
                    str(reddemPrice)+' rupees successfully completed. Your amount is credited in your bank account. Transaction ID : ' + \
                    str(inputs['transID']) + \
                    '. Any query visit https://crowdindia.co.in/contact.html'
                template_id = '1207161907157203553'
                # smsSend(phone, message, template_id)
                data = {
                    'name': name,
                    'email': email,
                    'subject': 'Power Successfully',
                    'message': 'Your Wallet balance withdrawal request of ' +
                    str(reddemPrice)+' rupees successfully completed. Your amount is credited in your bank account. Transaction ID : ' +
                    str(inputs['transID']) +
                    '. Any query visit https://crowdindia.co.in/contact.html',
                    'from_email': settings.EMAIL_HOST_USER
                }
                # Util.email_send(data)
                returnArr = {
                    'status': 'Withdrawal Request Completed.'
                }
            else:
                returnArr = {
                    'status': 'Insufficient Wallet Balance.'
                }
        else:
            returnArr = {
                'status': 'Withdrawal Request Not Found.'
            }

        return Response(returnArr)


class vendorPaymentCancel(views.APIView):
    def post(self, request):
        inputs = request.data
        withDraw = WalletWithdraw.objects.filter(
            id=inputs['withdraw_id']).first()
        if withDraw:
            reddemPrice = withDraw.amount
            userId = withDraw.user_id_id
            WalletWithdraw.objects.filter(id=inputs['withdraw_id']).update(
                status=3)
            userDetails = User.objects.filter(id=userId).first()
            phone = userDetails.phone
            email = userDetails.email
            name = userDetails.name
            message = 'Dear Customer, Your Wallet balance withdrawal request of ' + \
                str(reddemPrice) + \
                ' rupees canceled by admin. Any query visit https://crowdindia.co.in/contact.html'
            template_id = ''
            # smsSend(phone, message, template_id)
            data = {
                'name': name,
                'email': email,
                'subject': 'Power Successfully',
                'message': 'Your Wallet balance withdrawal request of ' + str(reddemPrice) + ' rupees canceled by admin. Any query visit https://crowdindia.co.in/contact.html',
                'from_email': settings.EMAIL_HOST_USER
            }
            # Util.email_send(data)
            returnArr = {
                'status': 'Withdrawal Request Canceled.'
            }
        else:
            returnArr = {
                'status': 'Withdrawal Request Not Found.'
            }

        return Response(returnArr)


def smsSend(phone, msg, template_id):
    response = requests.get("http://weberleads.in/http-tokenkeyapi.php?authentic-key="+settings.WEBERLEADS_API +
                            "&senderid="+settings.WEBERLEADS_SENDERID+"&route=2&number="+phone+"&message="+msg+"&templateid="+template_id)
    return(response)


class sendMail(views.APIView):
    def post(self, request):
        inputs = request.data
        name = inputs['name']
        email = inputs['email']
        subject = inputs['subject']
        message = inputs['message']
        data = {'name': name, 'email': email, 'subject': subject,
                'message': message, 'from_email': settings.EMAIL_HOST_USER}
        res = Util.email_send(data)
        print(res)
        if res:
            newArr = {
                'msg': 'Ticket Send Successfully.'
            }
        else:
            newArr = {
                'msg': 'Somthings Wrong. Please Try again later.'
            }
        return Response(newArr, status=status.HTTP_200_OK)


def emailView(request):
    return render(request, "email_template.html")


class adminPointTransction(views.APIView):
    def post(self, request):
        inputs = request.data
        userDetails=User.objects.filter(id=inputs['user_id'])
        if userDetails:
            wallet = Wallet.objects.filter(user_id_id=inputs['user_id']).first()
            if inputs['walletType']=='money':
                if inputs['type']=='CREDIT':
                    updatedWalletBalance=wallet.amount+int(inputs['point'])
                else:
                    updatedWalletBalance=wallet.amount-int(inputs['point'])

                if updatedWalletBalance>=0:
                    walletUpdate = Wallet.objects.filter(
                        user_id_id=inputs['user_id']).update(amount=updatedWalletBalance)
                    WalletTransCreate = WalletTransaction.objects.create(
                        user_id_id=inputs['user_id'], transactionAmount=int(inputs['point']), afterTransactionAmount=updatedWalletBalance, remarks=inputs['remarks'],walletType='MONEY', transactionType=inputs['type'])

                    newArr={
                        'status':True,
                        'msg':'Money '+str(inputs['type'])+' successfully.'
                    }
                else:
                    newArr={
                        'status':False,
                        'msg':'Insufficient Wallet Money'
                    }
            else:
                if inputs['type']=='CREDIT':
                    updatedWalletBalance=wallet.point+int(inputs['point'])
                else:
                    updatedWalletBalance=wallet.point-int(inputs['point'])

                if updatedWalletBalance>=0:
                    walletUpdate = Wallet.objects.filter(
                        user_id_id=inputs['user_id']).update(point=updatedWalletBalance)
                    WalletTransCreate = WalletTransaction.objects.create(
                        user_id_id=inputs['user_id'], transactionAmount=int(inputs['point']), afterTransactionAmount=updatedWalletBalance, remarks=inputs['remarks'],walletType='REWARDS', transactionType=inputs['type'])

                    newArr={
                        'status':True,
                        'msg':'Point '+str(inputs['type'])+' successfully.'
                    }
                else:
                    newArr={
                        'status':False,
                        'msg':'Insufficient Wallet Point'
                    }
        else:
            newArr={
                'status':False,
                'msg':'User not found'
            }
        return Response(newArr)