from django.urls import path
from . import views

urlpatterns = [
    path('service/', views.ServiceAPIView.as_view(), name='service'),
    path('service/<int:id>', views.ServiceAPIDetailsView.as_view(), name='serviceDetails'),
    path('vendorService/', views.viewAllServiceAPIView.as_view(), name='vendorService'),
    path('adminService/', views.viewAllServiceAdminAPIView.as_view(), name='adminService'),
    path('addService/', views.addServiceAPIView.as_view(), name='addService'),
    path('singleService/<int:id>', views.viewSingleServiceAdminAPIView.as_view(), name='singleService'),
    path('enquiry/', views.EnquiryAPIView.as_view(), name='enquiry'),
    path('enquiry/<int:id>', views.EnquiryAPIDetailsView.as_view(), name='enquiryDetails'),
    path('enquirySubmit/', views.EnquirySubmitAPIView.as_view(), name='enquirySubmit'),
    path('userService/', views.viewAllServiceUserAPIView.as_view(), name='userService'),
    path('singleServiceUser/<int:id>', views.viewSingleServiceUserAPIView.as_view(), name='singleServiceUser'),
    path('vendorEnquiry/', views.getVendorEnquiryAPIView.as_view(), name='vendorEnquiry'),
    path('adminEnquiry/', views.getAdminEnquiryAPIView.as_view(), name='adminEnquiry'),
    path('userEnquiry/', views.getUserEnquiryAPIView.as_view(), name='userEnquiry'),












]
