from rest_framework import serializers
from .models import VendorDetails, POSDetails, RewordPointForUser, MinimumOrderValueForUser
from authentication.models import User


class VendorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetails
        fields = ['id', 'user_id', 'aadharNumber', 'panNumber', 'companyName', 'companyLogo', 'gstNumber', 'aadharImage',
                  'panImage', 'vendorSign', 'vendorApproveStatus', 'ProfileUpdatePermission', 'POS']


class POSSerializer(serializers.ModelSerializer):
    class Meta:
        model = POSDetails
        fields = ['id', 'user_id', 'vendor_id', 'activeStatus']


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RewordPointForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewordPointForUser
        fields = '__all__'


class MinimumOrderValueForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinimumOrderValueForUser
        fields = '__all__'
