from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CouponSerializer, DisplayBannerSerializer,PromotionBannerSerializer
from rest_framework import permissions
from .models import Coupon, DisplayBanner, PromotionBanner


# Create your views here.
class CouponAPIView(ListCreateAPIView):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class CouponDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


# Create your views here.
class DisplayBannerAPIView(ListCreateAPIView):
    serializer_class = DisplayBannerSerializer
    queryset = DisplayBanner.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class DisplayBannerDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DisplayBannerSerializer
    queryset = DisplayBanner.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()
class PromotionBannerAPIView(ListCreateAPIView):
    serializer_class = PromotionBannerSerializer
    queryset = PromotionBanner.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class PromotionBannerDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PromotionBannerSerializer
    queryset = PromotionBanner.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()