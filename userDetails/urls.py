from django.urls import path
from . import views

urlpatterns = [
    path('vendor/', views.VendorDetailsAPIView.as_view(), name='vendor'),
    path('vendor/<int:id>', views.VendorDetailsAPIDetailsView.as_view(),
         name='vendorDetails'),
    path('pos/', views.POSAPIView.as_view(), name='pos'),
    path('pos/<int:id>', views.POSDetailsView.as_view(), name='posDetails'),
    path('user/<int:id>', views.UserDetailsView.as_view(), name='userDetails'),
    path('vendorres/', views.VendorResView.as_view(), name='vendorres'),
    path('alluser/', views.AllUserDetailsView.as_view(), name='alluser'),
    path('allvendoruser/', views.AllVendorUserDetailsView.as_view(),
         name='allvendoruser'),
    path('search/', views.SearchDetailsView.as_view(), name='search'),
    path('searchuser/', views.SearchallUserDetailsView.as_view(), name='searchuser'),
    path('alldeliveryboy/', views.AllDeliveryDetailsView.as_view(),
         name='alldeliveryboy'),
    path('showProfile/', views.DeliveryBoyDetailsView.as_view(), name='showProfile'),
    #     path('showReferUser/', views.ReferDetailsView.as_view(), name='showReferUser'),
    path('showReferUser/', views.RewardsListView.as_view(), name='showReferUser'),


    path('showUser/', views.UserDetails.as_view(), name='showUser'),
    path('subscribe/', views.subscribe.as_view(), name='subscribe'),
    path('subscribeFromAdmin/', views.subscribeFromAdmin.as_view(),
         name='subscribeFromAdmin'),

    path('UserDetailsAdmin/<int:id>',
         views.UserDetailsAdmin.as_view(), name='UserDetailsAdmin'),
    path('GetPlan/', views.GetPlan.as_view(), name='GetPlan'),
    path('PurchaseList/', views.PurchaseList.as_view(), name='PurchaseList'),
    #     path('sendCashBack/', views.sendCashBack.as_view(), name='PurchaseList'),
    path('sendCashBack/', views.sendCashBackNew.as_view(), name='PurchaseList'),

    path('reword/', views.RewordPointForUserAPIView.as_view(), name='reword'),
    path('reword/<int:id>', views.RewordPointForUserAPIDetailsView.as_view(),
         name='rewordDetails'),
    path('minimumOrderValue/', views.MinimumOrderValueForUserAPIView.as_view(),
         name='mimimumOrderValue'),
    path('minimumOrderValue/<int:id>', views.MinimumOrderValueForUserAPIDetailsView.as_view(),
         name='minimumOrderValueDetails'),
    path('checkUser/', views.CheckUser.as_view(), name='checkUser'),

]
