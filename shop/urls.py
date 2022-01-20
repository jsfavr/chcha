from django.urls import path
from . import views

urlpatterns = [
    path('shopPage/', views.shopPageAPIView.as_view(), name='shopPage'),
    path('filter_data/', views.AllShopAPIView.as_view(), name='filter_data'),


]
