from django.db import models
from authentication.models import User


# Create your models here.
class Wallet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    totalPoint = models.IntegerField(default=0)


class WalletTransaction(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    transactionAmount = models.IntegerField(default=0)
    afterTransactionAmount = models.IntegerField(default=0)
    remarks = models.CharField(max_length=100, null=True)
    transactionType = models.CharField(max_length=100, null=True)
    walletType = models.CharField(max_length=100, default='MONEY')
    updated_at = models.DateTimeField(auto_now=True)


class WalletWithdraw(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    transID = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class BankDetails(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bankName = models.CharField(max_length=150, null=True)
    AccountNumber = models.CharField(max_length=150, null=True)
    accountHolderName = models.CharField(max_length=250, null=True)
    ifscCode = models.CharField(max_length=150, null=True)
    branchName = models.CharField(max_length=250, null=True)
    upi = models.CharField(max_length=250, null=True)
