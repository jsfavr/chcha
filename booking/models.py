from django.db import models
from authentication.models import User
from product.models import Product
from address.models import ShippingAddress
import datetime

# Create your models here.


class BookingPayment(models.Model):
    grandTotal = models.IntegerField(default=0)
    subTotal = models.IntegerField(default=0)
    razorpayPaymentId = models.CharField(max_length=100)
    paymentType = models.CharField(max_length=20)
    deliveryCharge = models.IntegerField(default=0)
    walletAmount = models.IntegerField(default=0)
    walletPoint = models.IntegerField(default=0)
    couponDiscount = models.IntegerField(default=0)
    couponCode = models.CharField(max_length=20, null=True, blank=True)
    shippingAddressId = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Booking(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    productSellingPrice = models.DecimalField(
        default=1.0, decimal_places=10, max_digits=20)
    productGST = models.DecimalField(
        default=1.0, decimal_places=10, max_digits=20)
    productPayablePrice = models.IntegerField(default=0)
    orderID = models.CharField(max_length=120)
    deliveryCharge = models.IntegerField(default=0)
    walletAmount = models.IntegerField(default=0)
    walletPoint = models.IntegerField(default=0)
    couponDiscount = models.IntegerField(default=0)
    couponCode = models.CharField(max_length=20, null=True, blank=True)
    paymentType = models.CharField(max_length=20)
    orderStatus = models.IntegerField(default=1)
    razorpayPaymentId = models.CharField(max_length=100)
    shippingAddressId = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE)
    OrderDate = models.DateField(auto_now_add=True)
    deliveryDate = models.DateField(null=True, blank=True)
    returnDate = models.DateField(null=True, blank=True)
    orderInTransitDate = models.DateField(null=True, blank=True)
    outForDeliveryDate = models.DateField(null=True, blank=True)
    readyForReturnDate = models.DateField(null=True, blank=True)
    outForPicupDate = models.DateField(null=True, blank=True)
    cancelDate = models.DateField(null=True, blank=True)
    deliveryBoyName = models.CharField(max_length=100, default='')
    deliveryBoyPhone = models.CharField(max_length=100, default='')
    returnBoyName = models.CharField(max_length=100, default='')
    returnBoyPhone = models.CharField(max_length=100, default='')
    reviewStatus = models.BooleanField(default=False)
    redeemStatus = models.BooleanField(default=False)
    invoiceNumber = models.CharField(max_length=120, null=True)
    invoiceDate = models.DateField(null=True, blank=True)
    bookingPaymentID = models.ForeignKey(
        BookingPayment, on_delete=models.CASCADE)
    deliveryBoyId = models.IntegerField(default=1)
    returnBoyId = models.IntegerField(default=1)
    returnExpairStatus = models.BooleanField(default=False)


class Reason(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    reason = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
