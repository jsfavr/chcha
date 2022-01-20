from django.urls import path
from . import views

urlpatterns = [
    path('POSAllProductDelete/', views.POSAllProductDeleteAPIView.as_view(), name='POSAllProductDelete'),
    path('addToCart/', views.addToCartAPIView.as_view(), name='addToCart'),
    path('GetProduct/', views.GetProductAPIView.as_view(), name='GetProduct'),
    path('OrderSubmit/', views.OrderSubmitAPIView.as_view(), name='OrderSubmit'),
    path('OrderView/', views.OrderViewAPIView.as_view(), name='OrderView'),
    path('OrderViewVendor/', views.OrderViewVendorAPIView.as_view(), name='OrderViewVendor'),
    path('OrderViewDetails/', views.OrderViewDetailsAPIView.as_view(), name='OrderViewDetails'),







    









]
