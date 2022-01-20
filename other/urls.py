from django.urls import path
from . import views

urlpatterns = [
    path('review/', views.ReviewAPIView.as_view(), name='review'),
    path('review/<int:id>', views.ReviewAPIDetailsView.as_view(),
         name='reviewDetails'),
    path('subscribe/', views.SubscribeAPIView.as_view(), name='subscribeAddress'),
    path('subscribe/<int:id>', views.SubscribeAPIDetailsView.as_view(),
         name='subscribeDetails'),
    path('inventoryTransaction/', views.InventoryTransactionAPIView.as_view(),
         name='InventoryTransaction'),
    path('inventoryTransaction/<int:id>', views.InventoryTransactionAPIDetailsView.as_view(),
         name='InventoryTransactionDetails'),
    path('addStock/', views.AddStock.as_view(), name='AddStock'),
    path('reviewAdd/', views.userReviewAPIView.as_view(), name='reviewAdd'),
    path('getReview/', views.getReview.as_view(), name='getReview'),

    
    path('search/', views.userSearchAPIView.as_view(), name='search'),
    path('redeem/', views.vendorRedeemAPIView.as_view(), name='redeem'),
    path('AdminHighRatting/', views.AdminHighRattingAPIView.as_view(),
         name='AdminHighRatting'),
    path('AdminLowRatting/', views.AdminLowRattingAPIView.as_view(),
         name='AdminLowRatting'),
    path('AdminHome/', views.AdminHomeAPIView.as_view(), name='AdminHome'),
    path('VendorHome/', views.VendorHomeAPIView.as_view(), name='VendorHome'),
    path('search/', views.userSearchAPIView.as_view(), name='search'),
    path('searchByCode/', views.usersearchByCodeAPIView.as_view(), name='searchByCode'),
    path('POSAllProductDelete/', views.POSAllProductDeleteAPIView.as_view(),
         name='POSAllProductDelete'),
    path('notify/', views.NotifyMeAPIView.as_view(), name='notify'),
    path('notify/<int:id>', views.NotifyMeAPIDetailsView.as_view(),
         name='notifyDetails'),
    path('getsms/', views.LoginOTP.as_view(), name='getsms'),
    path('pincodeSearch/', views.pincodeSearchAPIView.as_view(), name='pincodeSearch'),
    path('delivery_home/', views.deliveryHomeAPIView.as_view(), name='pincodeSearch'),
    path('setting/', views.SettingsAPIView.as_view(), name='setting'),
    path('setting/<int:id>', views.SettingsAPIDetailsView.as_view(),
         name='settingDetails'),
    path('settingArr/', views.settingArrayAPIView.as_view(), name='settingArr'),
    path('paymentOption/', views.paymentOptionAPIView.as_view(),
         name='paymentOptionDetails'),
    path('paymentOption/<int:id>',
         views.paymentOptionAPIDetailsView.as_view(), name='settingArr'),
    path('paymentOptionArr/', views.paymentOptionArr.as_view(),
         name='paymentOptionArr'),
    path('AdminGraph/', views.AdminGraph.as_view(),
         name='AdminGraph'),










]
