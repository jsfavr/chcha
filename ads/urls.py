from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
# from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('video/', views.VideoAdsAPIView.as_view(), name='video'),
    path('video/<int:id>', views.VideoAdsDetailsAPIView.as_view(), name='videoDetails'),
    path('video/add/', views.AddVideoAds.as_view(), name='videoAdd'),
    path('video/views/', views.ViewVideoAds.as_view(), name='videoViews'),
    path('video/adminViews/', views.ViewAdminVideoAds.as_view(),
         name='videoAdminViews'),
    path('adsmanagement/', views.Adsmanagement.as_view(), name='adsmanagement'),
    path('power/video/category/',
         views.VideoCategoryAPIView.as_view(), name='category'),
    path('power/video/category/<int:id>',
         views.VideoCategoryDetailsAPIView.as_view(), name='categoryDetails'),
    path('power/video/', views.VideoAPIView.as_view(), name='powerVideo'),
    path('power/video/<int:id>', views.VideoDetailsAPIView.as_view(),
         name='powerVideoDetails'),
    path('power/video/keyField/', views.VideoKeyFieldAPIView.as_view(), name='video'),
    path('power/video/keyField/<int:id>',
         views.VideoKeyFieldDetailsAPIView.as_view(), name='videoDetails'),
    path('power/category/get/', views.powerCategory.as_view(), name='powerCategory'),
    path('power/video/get/', views.powerVideo.as_view(), name='powerVideo'),
    path('power/video/add/', views.powerVideoAdd.as_view(), name='powerVideoAdd'),
    path('power/video/get/<int:id>', views.powerVideoParticular.as_view(),
         name='powerVideoParticular'),
    path('power/video/categoryWise/',
         views.powerVideoCategory.as_view(), name='powerVideoCategory'),

]
