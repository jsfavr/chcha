from rest_framework import serializers
from .models import BankDetails, Wallet, WalletTransaction, WalletWithdraw


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = '__all__'


class WalletWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletWithdraw
        fields = '__all__'
