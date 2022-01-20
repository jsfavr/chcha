from django.urls import path
from . import views

urlpatterns = [
    path('shipping/', views.ShippingAddressAPIView.as_view(), name='shippingAddress'),
    path('shipping/<int:id>', views.ShippingAddressDetailsAPIView.as_view(), name='shippingAddressDetails'),
    path('billing/', views.BillingAddressAPIView.as_view(), name='billingAddress'),
    path('billing/<int:id>', views.BillingAddressDetailsAPIView.as_view(), name='billingAddressDetails'),
    path('deliveryPincode/', views.DeliveryPincodeAPIView.as_view(), name='deliveryPincode'),
    path('deliveryPincode/<int:id>', views.DeliveryPincodeDetailsAPIView.as_view(), name='deliveryPincodeDetails'),
    path('deliveryBoyPincode/', views.DeliveryBoyPincodeAPIView.as_view(), name='deliveryBoyPincode'),
    path('deliveryBoyPincode/<int:id>', views.DeliveryBoyPincodeDetailsAPIView.as_view(),name='deliveryBoyPincodeDetails'),
    path('delBoyPincodedetails/<int:id>', views.DeliveryBoyPincodeDetailsView.as_view(),name='delBoyPincodeDetails'),
    path('BillingAddressadd', views.DeliveryBillingAddressView.as_view(),name='BillingAddressadd'),
    path('FetchShippingAddress', views.FetchShippingAddressView.as_view(),name='FetchShippingAddress'),
    path('gerDeliveryBoy/<pincode>', views.userListPincode.as_view(),name='gerDeliveryBoy'),
    path('deliveryBoyPincodeAdd/', views.deliveryBoyPincodeADD.as_view(),name='deliveryBoyPincodeAdd')
]
