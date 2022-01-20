from rest_framework import serializers
from .models import Cart, NonCart, Wishlist


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user_id', 'product_id', 'quantity']


class NonCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonCart
        fields = ['user_id', 'product_id', 'quantity']


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['user_id', 'product_id']
