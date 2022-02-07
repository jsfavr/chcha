from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartAPIView.as_view(), name='cart'),
    path('cart/<int:id>', views.CartAPIDetailsView.as_view(), name='cartDetails'),
    path('nonCart/', views.NonCartAPIView.as_view(), name='nonCartAddress'),
    path('nonCart/<int:id>', views.NonCartAPIDetailsView.as_view(), name='nonCartDetails'),
    path('wishlist/', views.WishlistAPIView.as_view(), name='wishlistAddress'),
    path('wishlist/<int:id>', views.WishlistDetailsAPIView.as_view(), name='wishlistDetails'),
    path('useCartDetails/', views.UserCartView.as_view(), name='useCartDetails'),
    path('usewishlistDetails/', views.UserwishlistView.as_view(), name='usewishlistDetails'),
    path('WishlistToCartView/', views.WishlistToCartView.as_view(), name='WishlistToCartView'),
    path('addcart/', views.AddUserCart.as_view(), name='addcart'),
    path('addwishlist/', views.AddUserWishlist.as_view(), name='addwishlist'),
    path('totalcart/', views.CountCartlist.as_view(), name='totalcart'),
    path('totalwishlist/', views.CountWishlist.as_view(), name='totalwishlist'),
    path('checkwishlist/<id>', views.CheckWishlist.as_view(), name='checkwishlist'),
    path('checkcart/<id>', views.CheckCart.as_view(), name='checkcart'),
]
