from django.urls import path
from . import views

urlpatterns = [
    path('bank/', views.BankDetailsAPIView.as_view(), name='bank'),
    path('bank/<int:id>', views.BankDetailsDetailsAPIView.as_view(),
         name='bankDetails'),
    path('wallet/', views.WalletAPIView.as_view(), name='walletAddress'),
    path('wallet/<int:id>', views.WalletDetailsAPIView.as_view(),
         name='walletAddressDetails'),
    path('transaction/', views.WalletTransactionAPIView.as_view(), name='transaction'),
    path('transaction/<int:id>', views.WalletTransactionDetailsAPIView.as_view(),
         name='transactionDetails'),
    path('withdraw/', views.WalletWithdrawAPIView.as_view(), name='withdraw'),
    path('withdraw/<int:id>', views.WalletWithdrawDetailsAPIView.as_view(),
         name='withdrawDetails'),
    path('walletamount/', views.WalletGetAPI.as_view(), name='walletamount'),
    path('wallettransection/', views.WalletTransectionGetAPI.as_view(),
         name='wallettransection'),
    path('bankshow/', views.WalletBankGetAPI.as_view(), name='bankshow'),
    path('getwithdraw/', views.WalletWithdrawGetAPI.as_view(), name='getwithdraw'),
    path('vendorwithdraw/', views.vendorWithdrawRequest.as_view(),
         name='vendorwithdraw'),
    path('vendorpayment/', views.vendorPayment.as_view(), name='vendorpayment'),
    path('vendorPaymentCancel/', views.vendorPaymentCancel.as_view(),
         name='vendorPaymentCancel'),
    path('sendMail/', views.sendMail.as_view(), name='sendMail'),
    path('emailView/', views.emailView, name='emailView'),
    path('adminPointTransction/', views.adminPointTransction.as_view(), name='adminPointTransction'),

]
