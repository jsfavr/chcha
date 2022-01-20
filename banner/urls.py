from django.urls import path
from . import views

urlpatterns = [
    path('coupon/', views.CouponAPIView.as_view(), name='coupon'),
    path('coupon/<int:id>', views.CouponDetailsAPIView.as_view(), name='couponDetails'),
    path('display/', views.DisplayBannerAPIView.as_view(), name='display'),
    path('display/<int:id>', views.DisplayBannerDetailsAPIView.as_view(), name='displayDetails'),
    path('promotion/', views.PromotionBannerAPIView.as_view(), name='promotion'),
    path('promotion/<int:id>', views.PromotionBannerDetailsAPIView.as_view(), name='promotionDetails'),

]
