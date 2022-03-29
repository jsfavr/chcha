from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CartSerializer, WishlistSerializer, NonCartSerializer
from rest_framework import permissions, views, status
from .models import Cart, NonCart, Wishlist
from product.permissions import IsOwner
from django.core import serializers
from rest_framework.response import Response
from product.models import Product, ProductImage
from authentication.models import User
from userDetails.models import VendorDetails
from category.models import SubCategory


from rest_framework.response import Response

# Create your views here.


class CartAPIView(ListCreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class CartAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class NonCartAPIView(ListCreateAPIView):
    serializer_class = NonCartSerializer
    queryset = NonCart.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class NonCartAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = NonCartSerializer
    queryset = NonCart.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


# Create your views here.
class WishlistAPIView(ListCreateAPIView):
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class WishlistDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class UserCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id
        cart_item = Cart.objects.filter(user_id_id=user_id)
        modifiedProduct = []
        for eachProd in cart_item:
            cart = Cart.objects.filter(id=eachProd.id)
            product = Product.objects.filter(id=eachProd.product_id_id)
            for eachProd1 in product:
                vendor = VendorDetails.objects.filter(
                    user_id_id=eachProd1.user_id_id)
                subcatdel = SubCategory.objects.filter(
                    id=eachProd1.sub_cat_id_id)

            image = ProductImage.objects.filter(
                productID_id=eachProd.product_id_id)

            cartDetails = serializers.serialize('json', cart)
            productDetails = serializers.serialize('json', product)
            vendorDetails = serializers.serialize('json', vendor)
            imageDetails = serializers.serialize('json', image)
            subCat = serializers.serialize('json', subcatdel)

            cart1 = Cart.objects.filter(id=eachProd.id).first()
            product1 = Product.objects.filter(
                id=eachProd.product_id_id).first()
            if cart1.quantity > product1.availableStock:
                outOfStock = True
            else:
                outOfStock = False
            newrel = {
                'cartDetails': cartDetails,
                'productDetails': productDetails,
                'vendorDetails': vendorDetails,
                'imageDetails': imageDetails,
                'subCat': subCat,
                'outOfStock': outOfStock
            }
            modifiedProduct.append(newrel)

        return Response(modifiedProduct)


class UserwishlistView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id
        cart_item = Wishlist.objects.filter(user_id_id=user_id)
        modifiedProduct = []
        for eachProd in cart_item:
            cart = Wishlist.objects.filter(id=eachProd.id)
            product = Product.objects.filter(id=eachProd.product_id_id)
            for eachProd1 in product:
                vendor = VendorDetails.objects.filter(
                    user_id_id=eachProd1.user_id_id)
                subcatdel = SubCategory.objects.filter(
                    id=eachProd1.sub_cat_id_id)

            image = ProductImage.objects.filter(
                productID_id=eachProd.product_id_id)

            cartDetails = serializers.serialize('json', cart)
            productDetails = serializers.serialize('json', product)
            vendorDetails = serializers.serialize('json', vendor)
            imageDetails = serializers.serialize('json', image)
            subCat = serializers.serialize('json', subcatdel)

            newrel = {
                'cartDetails': cartDetails,
                'productDetails': productDetails,
                'vendorDetails': vendorDetails,
                'imageDetails': imageDetails,
                'subCat': subCat


            }
            modifiedProduct.append(newrel)

        return Response(modifiedProduct)


class WishlistToCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        wishlist_item = Cart.objects.filter(
            user_id_id=user_id, product_id_id=inputs['product_id'])
        if wishlist_item:
            Wishlist.objects.filter(id=inputs['id']).delete()
            return Response({'wishlist': 'Item Already Added'}, status=status.HTTP_200_OK)
        else:
            Cart.objects.create(
                product_id_id=inputs['product_id'], user_id_id=user_id, quantity=1)
            Wishlist.objects.filter(id=inputs['id']).delete()
            return Response({'wishlist': 'Item Successfully Added'}, status=status.HTTP_200_OK)


class AddUserCart(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        user_cart = Cart.objects.filter(user_id_id=user_id)
        isCart = False
        proGet = Product.objects.filter(id=inputs['product_id']).first()
        for eachProd in user_cart:
            cart = Cart.objects.filter(id=eachProd.id)
            product = Product.objects.filter(id=eachProd.product_id_id)
            for eachProd1 in product:
                if eachProd1.user_id_id == proGet.user_id_id:
                    isCart = True
                else:
                    isCart = False
        if user_cart:
            if isCart:      
                cart_item = Cart.objects.filter(
                    user_id_id=user_id, product_id_id=inputs['product_id'])
                if cart_item:
                    cart_data = Cart.objects.filter(
                        user_id_id=user_id, product_id_id=inputs['product_id']
                    ).update(
                        quantity=inputs['quantity'])
                    return Response({'cart': 'Item Already Updated'}, status=status.HTTP_200_OK)
                else:
                    cart_data = Cart.objects.create(
                        quantity=inputs['quantity'], product_id_id=inputs['product_id'], user_id_id=user_id)
                    return Response({'cart': 'Item Successfully Added'}, status=status.HTTP_200_OK)
            else:
                return Response({'cart': 'Cart Item Always be same Vendor'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cart_item = Cart.objects.filter(
                user_id_id=user_id, product_id_id=inputs['product_id'])
            if cart_item:
                cart_data = Cart.objects.filter(
                    user_id_id=user_id, product_id_id=inputs['product_id']
                ).update(
                    quantity=inputs['quantity'])
                return Response({'cart': 'Item Already Updated'}, status=status.HTTP_200_OK)
            else:
                cart_data = Cart.objects.create(
                    quantity=inputs['quantity'], product_id_id=inputs['product_id'], user_id_id=user_id)
                return Response({'cart': 'Item Successfully Added'}, status=status.HTTP_200_OK)


class AddUserWishlist(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        user_cart = Wishlist.objects.filter(user_id_id=user_id)
        isCart = False
        proGet = Product.objects.filter(id=inputs['product_id']).first()
        for eachProd in user_cart:
            cart = Wishlist.objects.filter(id=eachProd.id)
            product = Product.objects.filter(id=eachProd.product_id_id)
            for eachProd1 in product:
                if eachProd1.user_id_id == proGet.user_id_id:
                    isCart = True
                else:
                    isCart = False
        if user_cart:
            if isCart: 
                wishlist_item = Wishlist.objects.filter(
                    user_id_id=user_id, product_id_id=inputs['product_id'])
                if wishlist_item:
                    return Response({'wishlist': 'Item Already Added'}, status=status.HTTP_200_OK)
                else:
                    wishlist_data = Wishlist.objects.create(
                        product_id_id=inputs['product_id'], user_id_id=user_id)
                    return Response({'wishlist': 'Item Successfully Added'}, status=status.HTTP_200_OK)
            else:
                return Response({'wishlist': 'wishlist Item Always be same Vendor'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            wishlist_item = Wishlist.objects.filter(
                user_id_id=user_id, product_id_id=inputs['product_id'])
            if wishlist_item:
                return Response({'wishlist': 'Item Already Added'}, status=status.HTTP_200_OK)
            else:
                wishlist_data = Wishlist.objects.create(
                    product_id_id=inputs['product_id'], user_id_id=user_id)
                return Response({'wishlist': 'Item Successfully Added'}, status=status.HTTP_200_OK)
                


class CountCartlist(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get(self, request):
        user_id = self.request.user.id
        total_cardlist = Cart.objects.filter(user_id_id=user_id).count()
        return Response({'total_cardlist': total_cardlist}, status=status.HTTP_200_OK)


class CountWishlist(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id
        total_wishlist = Wishlist.objects.filter(user_id_id=user_id).count()
        return Response({'total_wishlist':  total_wishlist}, status=status.HTTP_200_OK)


class CheckCart(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, id):
        pid = id
        user_id = self.request.user.id
        cart_item = Cart.objects.filter(user_id_id=user_id, product_id_id=pid)
        if cart_item:
            return Response({'cart': 'Item Already Added'}, status=status.HTTP_200_OK)
        else:
            return Response({'cart': 'Item Not Added'}, status=status.HTTP_200_OK)


class CheckWishlist(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, id):
        pid = id
        user_id = self.request.user.id
        wishlist_item = Wishlist.objects.filter(
            user_id_id=user_id, product_id_id=pid)
        if wishlist_item:
            return Response({'wishlist': 'Item Already Added'}, status=status.HTTP_200_OK)
        else:
            return Response({'wishlist': 'Item Not Added'}, status=status.HTTP_200_OK)
