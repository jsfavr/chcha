from rest_framework import serializers
from .models import Coupon, DisplayBanner, PromotionBanner


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id','title', 'discount', 'couponImage', 'couponCode','couponValidDate','minPrice','couponType', 'activeStatus']


class DisplayBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplayBanner
        fields = ['id','image']
class PromotionBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionBanner
        fields = '__all__'