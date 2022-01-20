from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.BookingAPIView.as_view(), name='submit'),
    path('submit/<int:id>', views.BookingAPIDetailsView.as_view(),
         name='submitDetails'),
    path('reason/', views.ReasonAPIView.as_view(), name='reason'),
    path('reason/<int:id>', views.ReasonAPIDetailsView.as_view(),
         name='reasonDetails'),
    path('userBooking', views.userBookingAPIView.as_view(), name='userBooking'),
    path('userCancelBooking', views.userCancelBookingAPIView.as_view(),
         name='userCancelBooking'),
    path('userReturnBooking', views.userReturnBookingAPIView.as_view(),
         name='userReturnBooking'),
    path('vendorBooking/<status>',
         views.vendorBookingAPIView.as_view(), name='vendorBooking'),
    path('search/', views.vendorsearchBookingAPIView.as_view(), name='search'),
    path('bookingDetails/<id>', views.userSingleBookingAPIView.as_view(),
         name='bookingDetails'),
    path('newBookingDetails/<id>/<status>',
         views.vendorWiseBookingDetails.as_view(), name='bookingDetails'),
    path('salesReport/', views.salesReportAPIView.as_view(), name='salesReport'),
    path('taxsReport/', views.taxsReportAPIView.as_view(), name='taxsReport'),
    path('adminBooking/<status>',
         views.adminBookingAPIView.as_view(), name='adminBooking'),
    path('searchBooking/', views.SearchBookingAPIView.as_view(), name='searchBooking'),
    path('salesReportVendor/', views.salesReportVendorAPIView.as_view(),
         name='salesReportVendor'),
    path('taxsReportVendor/', views.taxsReportVendorAPIView.as_view(),
         name='taxsReportVendor'),
    path('bookingHistory/', views.bookingHistory.as_view(), name='bookingHistory'),
    path('deliveryReport/', views.deleveryBookingAPIView.as_view(),
         name='deliveryReport'),
    path('deliveryboyReport/<id>', views.deleveryReportAPIView.as_view(),
         name='deliveryboyReport'),
    path('retunboyReport/<id>',
         views.returnReportBookingAPIView.as_view(), name='retunboyReport'),
    path('deliveryBoyBooking/', views.deliveryBoyBookingAPIView.as_view(),
         name='deliveryBoyBooking'),
    path('deliveryBoyPendingBooking/', views.deliveryBoyPendingBookingAPIView.as_view(),
         name='deliveryBoyPendingBooking'),
    path('deliveryBoyCompleteBooking/', views.deliveryBoyCompleteBookingAPIView.as_view(),
         name='deliveryBoyCompleteBooking'),
    path('deliveryBoyCompleteReturnBooking/', views.deliveryBoyCompleteReturnBookingAPIView.as_view(),
         name='deliveryBoyCompleteReturnBooking'),
    path('deliveryBoyPendingReturnBooking/', views.deliveryBoyPendingReturnBookingAPIView.as_view(),
         name='deliveryBoyPendingReturnBooking'),
    path('bookingDetailsOrderId/<id>',
         views.userSingleBookingOrderIdAPIView.as_view(), name='bookingDetailsOrderId'),
    path('statusChange/<orderID>',
         views.statusChange.as_view(), name='statusChange'),
    path('invoiceGenerate/<orderID>',
         views.invoiceGenerate.as_view(), name='invoiceGenerate'),
    path('InvoiceBookingDetails/<id>',
         views.InvoiceBookingDetails.as_view(), name='InvoiceBookingDetails')


]
