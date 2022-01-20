from rest_framework import serializers
from .models import ShippingAddress, BillingAddress, DeliveryBoyPincode, DeliveryPincode


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id','user_id', 'pincode', 'flat', 'address', 'location', 'landmark', 'city', 'district', 'state', 'name',
                  'phone', 'optionalPhone']


class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = ['id','user_id', 'pincode', 'flat', 'address', 'location', 'city', 'district', 'state']


class DeliveryPincodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPincode
        fields = '__all__'


class DeliveryBoyPincodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryBoyPincode
        fields = '__all__'
