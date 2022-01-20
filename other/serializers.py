from rest_framework import serializers
from .models import Review, Subscribe, InventoryTransaction, NotifyMe, Settings, paymentOption


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['user_id']


class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = ['id', 'product_id', 'quantity', 'afterTransactionQuantity',
                  'remarks', 'transactionType', 'transactionDate', 'transactionID']


class NotifyMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotifyMe
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'


class paymentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = paymentOption
        fields = '__all__'
