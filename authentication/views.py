from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework import response
from .serializers import SetNewPasswordSerializer, RegisterSerializer, RegisterVendorSerializer, \
    RegisterAdminSerializer, RegisterPosSerializer, LoginvendorSerializer, LoginadminSerializer, RegisterPosSerializer, \
    LoginboySerializer, LoginposSerializer, RegisterDelboySerializer, LoginuserSerializer, EmailVerificationSerializer, \
    ResetPasswordSerialiizer, LoginotpuserSerializer, LoginotpadminSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import make_password
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import serializers
from userDetails.models import POSDetails
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
import json
import requests
from wallet.views import smsSend

from product.permissions import IsOwner


from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import shortuuid
# Create your views here.


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        referUserID = 0
        su = shortuuid.ShortUUID(alphabet="01345678")
        # print(su.random(length=6))
        # return response(True)
        if len(user['refer_code']) > 5:
            referDetails = User.objects.filter(
                username=user['refer_code']).first()
            if referDetails:
                referUserID = referDetails.id
        # print(user)
        user._mutable = True
        user['role_id'] = 1
        user['username'] = su.random(length=6)
        user['referUserID'] = referUserID
        user['is_verified'] = 1
        user['password'] = make_password(user['phone'])
        user._mutable = False

        # print(user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        # sms_body = 'Welcome ' + user.name + \
        #     ', You are successfully register on Crowd. Please download our apps https://crowdindia.co.in/app/download'
        # response = requests.get(
        #     "http://weberleads.in/http-tokenkeyapi.php?authentic-key=3134696e7374616e745f6765747761793631321586003895&senderid=INGWAY&route=2&number="+user.phone+"&message="+sms_body)
        # # absurl = 'http://' + current_site + relativeLink + '?token=' + str(token)
        # email_body = 'Hi ' + user.username + ' Use link below to verify your email\n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify Your Email'}
        # Util.send_email(data)

        message = 'Welcome ' + user.name + \
            ', You are successfully register on Crowd. Please download our apps https://crowdindia.co.in/app/download'
        template_id = '1207161907105543463'
        smsSend(user.phone, message, template_id)
        data = {
            'name': user.name,
            'email': user.email,
            'subject': 'Register Successfully',
            'message': 'Welcome ' + user.name +
            ', You are successfully register on Crowd. Please download our apps https://crowdindia.co.in/app/download',
            'from_email': settings.EMAIL_HOST_USER
        }
        Util.email_send(data)

        return Response(user_data, status=status.HTTP_200_OK)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully Activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Link Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Activation Link Invalid'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterVendorView(generics.GenericAPIView):
    serializer_class = RegisterVendorSerializer

    def post(self, request):
        user = request.data
        user['password'] = make_password(user['password'])
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        # sms_body = 'Welcome ' + user.name + \
        #     ', You are successfully register on Crowd as a Vendor. Please wait for admin approval. Any query visit https://crowdindia.co.in/contact.html'
        # response = requests.get(
        #     "http://weberleads.in/http-tokenkeyapi.php?authentic-key=3134696e7374616e745f6765747761793631321586003895&senderid=INGWAY&route=2&number="+user.phone+"&message="+sms_body)
        # # absurl = 'http://' + current_site + relativeLink + '?token=' + str(token)
        # email_body = 'Hi ' + user.username + ' Use link below to verify your email\n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify Your Email'}
        # Util.send_email(data)
        message = 'Welcome ' + user.name + \
            ', You are successfully register on Crowd as a Vendor. Please wait for admin approval. Any query visit https://crowdindia.co.in/contact.html'
        template_id = '1207161907136672146'
        smsSend(user.phone, message, template_id)
        data = {
            'name': user.name,
            'email': user.email,
            'subject': 'Register Successfully',
            'message': 'Welcome ' + user.name +
            ', You are successfully register on Crowd as a Vendor. Please wait for admin approval. Any query visit https://crowdindia.co.in/contact.html',
            'from_email': settings.EMAIL_HOST_USER
        }
        Util.email_send(data)
        return Response(user_data, status=status.HTTP_200_OK)


class RegisterAdminView(generics.GenericAPIView):
    serializer_class = RegisterAdminSerializer

    def post(self, request):
        user = request.data
        user['password'] = make_password(user['password'])
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_200_OK)


class RegisterPosView(generics.GenericAPIView):
    serializer_class = RegisterPosSerializer

    def post(self, request):
        user = request.data
        user['password'] = make_password(user['password'])
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        # absurl = 'http://' + current_site + relativeLink + '?token=' + str(token)
        # email_body = 'Hi ' + user.username + ' Use link below to verify your email\n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify Your Email'}
        # Util.send_email(data)

        return Response(user_data, status=status.HTTP_200_OK)


class RegisterDelboyView(generics.GenericAPIView):
    serializer_class = RegisterDelboySerializer

    def post(self, request):
        user = request.data
        user['password'] = make_password(user['password'])
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        sms_body = 'Welcome ' + user.name + \
            ', You are successfully register on Crowdindia as a Delivery Boy. Please wait for admin approval.'
        response = requests.get(
            "http://weberleads.in/http-tokenkeyapi.php?authentic-key=3134696e7374616e745f6765747761793631321586003895&senderid=INGWAY&route=2&number="+user.phone+"&message="+sms_body)
        # absurl = 'http://' + current_site + relativeLink + '?token=' + str(token)
        # email_body = 'Hi ' + user.username + ' Use link below to verify your email\n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify Your Email'}
        # Util.send_email(data)

        return Response(user_data, status=status.HTTP_200_OK)


class LoginuserView(generics.GenericAPIView):
    serializer_class = LoginuserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_200_OK)


class LoginotpuserView(generics.GenericAPIView):
    serializer_class = LoginotpuserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.data
        return Response(user_data, status=status.HTTP_200_OK)


class LoginotpadminView(generics.GenericAPIView):
    serializer_class = LoginotpadminSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.data
        return Response(user_data, status=status.HTTP_200_OK)


class LogiotpView(views.APIView):
    def post(self, request):
        inputs = request.data
        check_phone = User.objects.filter(phone=inputs['phone'])
        if check_phone:
            return Response({'msg': 'Phone found'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Phone not found'}, status=status.HTTP_200_OK)


class LogiotpadminView(views.APIView):
    def post(self, request):
        inputs = request.data
        check_phone = User.objects.filter(phone=inputs['phone'], role_id=3)
        if check_phone:
            return Response({'msg': 'Phone found'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Phone not found'}, status=status.HTTP_200_OK)


class LoginvendorView(generics.GenericAPIView):
    serializer_class = LoginvendorSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_200_OK)


class LoginadminView(generics.GenericAPIView):
    serializer_class = LoginadminSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_200_OK)


class LoginposView(generics.GenericAPIView):
    serializer_class = LoginposSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_200_OK)


class LoginboyView(generics.GenericAPIView):
    serializer_class = LoginboySerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordSerialiizer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = user.id
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello, \n Use link bellow to reset your password\n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset Password'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = uidb64
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid'}, status=status.HTTP_401_OK)
            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid'}, status=status.HTTP_401_OK)


class SetNewPasswordAPIview(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class PosDetailsAPIview(generics.GenericAPIView):
    def get(self, request, id):
        pid = id
        image = POSDetails.objects.filter(vendor_id_id=id)
        data = []
        for eachProd in image:
            data = User.objects.filter(id=eachProd.user_id_id)

        modifiedProduct = serializers.serialize('json', image)
        modifiedData = serializers.serialize('json', data)
        newPro = {
            'posDetails': modifiedProduct,
            'posUserDetails': modifiedData,
        }
        return Response(newPro)


class AuthenticationCheckView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        user = self.request.user
        if(self.request.user):
            return Response({'success': True, 'message': 'Athentication Found', 'User': user.email}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'Athentication not Found'}, status=status.HTTP_404_NOT_FOUND)


class EmailSendAPI(views.APIView):
    def post(self, request):
        inputs = request.data
        subject = inputs['subject']
        content = inputs['body']
        to_email = inputs['to_email']
        data = {'title': subject, 'content': content, 'email_subject': subject,
                'to_email': to_email, 'from_email': settings.EMAIL_HOST_USERS}
        Util.email_send(data)
        return Response({'msg': 'Successfully Sent Mail'}, status=status.HTTP_200_OK)


class ForgotSendAPI(views.APIView):
    def post(self, request):
        inputs = request.data
        user = User.objects.filter(email=inputs['email'], role_id=2).first()
        if user:
            phone = user.phone
            return Response(phone)
        else:
            return Response(0)


def emailView(request):
    return render(request, "email.html")


class updateReffer(views.APIView):
    def post(self, request):
        inputs = request.data
        userDetails = User.objects.filter(id=inputs['id']).first()
        if userDetails.username == inputs['refer_code']:
            returnArr = {
                'msg': 0
            }
        else:
            referUserDetails = User.objects.filter(
                username=inputs['refer_code']).first()
            if referUserDetails:
                if referUserDetails.role_id == 1:
                    if referUserDetails.subscriptionStatus:
                        User.objects.filter(id=inputs['id']).update(
                            refer_code=inputs['refer_code'],
                            referUserID=referUserDetails.id
                        )
                        returnArr = {
                            'msg': 1
                        }
                    else:
                        returnArr = {
                            'msg': 3
                        }
                else:
                    returnArr = {
                        'msg': 4
                    }
            else:
                returnArr = {
                    'msg': 2
                }
        return Response(returnArr)
