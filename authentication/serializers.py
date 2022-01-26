from rest_framework import serializers,status
from .models import User
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import Util
from django.contrib.auth.hashers import make_password,check_password
import json
from rest_framework.response import Response
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id','name', 'username', 'email', 'password', 'phone', 'role_id','refer_code','is_verified','referUserID']

        def validate(self, attrs):
            email = attrs.get('email', '')
            username = attrs.get('username', '')
            phone = attrs.get('phone', '')
            name = attrs.get('name', '')
            role_id = attrs.get('role_id', '')
            refer_code = attrs.get('refer_code', '')
            referUserID = attrs.get('referUserID', '')


            if not username.isalnum():
                raise serializers.ValidationError('Username should contain letters and numbers')
            return attrs

        def create(self, validated_data):
            return User.objects.create_user(**validated_data)


class RegisterVendorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id','name', 'username', 'email', 'password', 'phone', 'role_id','status']

        def validate(self, attrs):
            email = attrs.get('email', '')
            username = attrs.get('username', '')
            phone = attrs.get('phone', '')
            name = attrs.get('name', '')
            role_id = attrs.get('role_id', '')
            status = attrs.get('status','')
            if not username.isalnum():
                raise serializers.ValidationError('Username should contain letters and numbers')
            return attrs

        def create(self, validated_data):
            return User.objects.create_vendor(**validated_data)


class RegisterAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'phone', 'role_id']

        def validate(self, attrs):
            email = attrs.get('email', '')
            username = attrs.get('username', '')
            phone = attrs.get('phone', '')
            name = attrs.get('name', '')
            role_id = attrs.get('role_id', '')
            if not username.isalnum():
                raise serializers.ValidationError('Username should contain letters and numbers')
            return attrs

        def create(self, validated_data):
            return User.objects.create_admin_user(**validated_data)


class RegisterPosSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id','name', 'username', 'email', 'password', 'phone', 'role_id','is_verified']

        def validate(self, attrs):
            email = attrs.get('email', '')
            username = attrs.get('username', '')
            phone = attrs.get('phone', '')
            name = attrs.get('name', '')
            role_id = attrs.get('role_id', '')
            if not username.isalnum():
                raise serializers.ValidationError('Username should contain letters and numbers')
            return attrs

        def create(self, validated_data):
            return User.objects.create_pos(**validated_data)


class RegisterDelboySerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id','name', 'username', 'email', 'password', 'phone', 'role_id', 'status','is_verified']

        def validate(self, attrs):
            email = attrs.get('email', '')
            username = attrs.get('username', '')
            phone = attrs.get('phone', '')
            name = attrs.get('name', '')
            role_id = attrs.get('role_id', '')
            status = attrs.get('status','')
            is_verified = attrs.get('is_verified','')
            if not username.isalnum():
                raise serializers.ValidationError('Username should contain letters and numbers')
            return attrs

        def create(self, validated_data):
            return User.objects.create_delboy(**validated_data)


class LoginuserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    name = serializers.CharField(max_length=255, min_length=8, read_only=True)
    tokens = serializers.CharField(max_length=255, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['id','name','email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials', 'try again')
        if not user.is_active:
            raise AuthenticationFailed('Account Disabled', 'try again')

        if not user.role_id == 1:
            raise AuthenticationFailed('You are not a user')

        if not user.is_verified:
            raise AuthenticationFailed('Email not Verified', 'try again')

        return {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'tokens': user.tokens,
        }
        return super().validate(attrs)
class LoginotpuserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=10, min_length=10, read_only=True)
    phone = serializers.CharField(max_length=10, min_length=10)
    tokens = serializers.CharField(max_length=255, min_length=8, read_only=True)
    name = serializers.CharField(max_length=255, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['id','email','phone','name','tokens']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        check_phone = User.objects.filter(phone=phone)
        for users in check_phone:
            email=users.email
        if check_phone:
            user = auth.authenticate(email=email,password=phone)
        
            if not user:
                raise AuthenticationFailed('Invalid credentials', 'try again')
            if not user.is_active:
                raise AuthenticationFailed('Account Disabled', 'try again')

            if not user.role_id == 1:
                raise AuthenticationFailed('You are not a user')

            if not user.is_verified:
                raise AuthenticationFailed('Email not Verified', 'try again')
        else:
            raise AuthenticationFailed('Phone No Invalid', 'try again')
        return {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'phone':users.phone,
            'tokens':user.tokens,
        }
class LoginotpadminSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=10, min_length=10, read_only=True)
    phone = serializers.CharField(max_length=10, min_length=10)
    tokens = serializers.CharField(max_length=255, min_length=8, read_only=True)
    name = serializers.CharField(max_length=255, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['id','email','phone','name','tokens']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        check_phone = User.objects.filter(phone=phone)
        for users in check_phone:
            email=users.email
        if check_phone:
            user = auth.authenticate(email=email,password=phone)
            if not user:
                raise AuthenticationFailed('Invalid credentials', 'try again')
            if not user.role_id == 3:
                raise AuthenticationFailed('You are not a admin')
        else:
            raise AuthenticationFailed('Phone No Invalid', 'try again')

        return {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'phone':users.phone,
            'tokens': user.tokens,
        }

class LoginvendorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    tokens = serializers.CharField(max_length=255, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['id','email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials', 'try again')
        if not user.is_active:
            raise AuthenticationFailed('Account Disabled', 'try again')

        if not user.role_id == 2:
            raise AuthenticationFailed('You are not a vendor')

        if not user.status == 1:
            raise AuthenticationFailed('Wait for admin approval')

        if not user.is_verified:
            raise AuthenticationFailed('Email not Verified', 'try again')

        return {
            'email': user.email,
            'id': user.id,
            'username': user.username,
            'tokens': user.tokens
        }
        return super().validate(attrs)


class LoginadminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    tokens = serializers.CharField(max_length=255, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials', 'try again')
        if not user.is_active:
            raise AuthenticationFailed('Account Disabled', 'try again')

        if not user.role_id == 3:
            raise AuthenticationFailed('You are not an admin')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
        return super().validate(attrs)


class LoginposSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    tokens = serializers.CharField(max_length=255, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['id','email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials', 'try again')
        if not user.is_active:
            raise AuthenticationFailed('Account Disabled', 'try again')

        if not user.role_id == 4:
            raise AuthenticationFailed('You are not a user')

        if not user.is_verified:
            raise AuthenticationFailed('Email not Verified', 'try again')

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
        return super().validate(attrs)


class LoginboySerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=10, min_length=10, read_only=True)
    phone = serializers.CharField(max_length=10, min_length=10)
    tokens = serializers.CharField(max_length=255, min_length=8, read_only=True)
    name = serializers.CharField(max_length=255, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['id','email','phone','name','tokens']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        check_phone = User.objects.filter(phone=phone)
        for users in check_phone:
            email=users.email
        if check_phone:
            user = auth.authenticate(email=email,password=phone)
            if not user:
                raise AuthenticationFailed('Invalid credentials', 'try again')
            if not user.is_active:
                raise AuthenticationFailed('Account Disabled', 'try again')
            if not user.role_id == 5:
                raise AuthenticationFailed('You are not a Delivery Boy')
            if not user.status == 1:
                raise AuthenticationFailed('Wait for admin approval')
            if not user.is_verified:
                raise AuthenticationFailed('Email not Verified', 'try again')
        else:
            raise AuthenticationFailed('Phone No Invalid', 'try again')

        return {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'phone':users.phone,
            'tokens': user.tokens,
        }
        return super().validate(attrs)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class ResetPasswordSerialiizer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=8,write_only=True)
    phone=serializers.IntegerField(write_only=True)
    
    class Meta:
        fields = ['password','phone']
    
    def validate(self,attrs):
        password = attrs.get('password')
        phone = attrs.get('phone')
        user = User.objects.get(phone=phone)
        passwd = make_password(password)    
        if not user:
            raise AuthenticationFailed('Your Phone No Invalid',401)
        user.password = passwd
        user.save()
        return (user)
        return super().validate(attrs)
        
