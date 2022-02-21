from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.checkoutItemsAPIView.as_view(), name='items'),
    path('findDeliveryCharge/', views.findDeliveryChargeAPIView.as_view(), name='findDeliveryCharge'),
    path('findCouponAvailability/', views.findCouponAvailabilityAPIView.as_view(), name='findCouponAvailability'),
    path('paymentCapture/', views.paymentCaptureAPIView.as_view(), name='paymentCapture'),
    path('orderSubmit/', views.orderSubmitAPIView.as_view(), name='orderSubmit'),
]
