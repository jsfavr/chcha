from django.urls import path, include
from . import views
from .router import router
urlpatterns = [
    path('brand/', views.ProductBrandAPIView.as_view(), name='productBrand'),
    path('brand/<int:id>', views.ProductBrandDetailsAPIView.as_view(),
         name='productBrandDetails'),
    path('group/', views.ProductGroupAPIView.as_view(), name='productGroup'),
    path('group/<int:id>', views.ProductGroupDetailsAPIView.as_view(),
         name='productGroupDetails'),
    path('product/', views.ProductAPIView.as_view(), name='product'),
    path('product/<int:id>', views.ProductDetailsAPIView.as_view(),
         name='productDetails'),
    path('image/', views.ProductImageAPIView.as_view(), name='productImage'),
    path('image/<int:id>', views.ProductImageDetailsAPIView.as_view(),
         name='productImageDetails'),
    path('feature/', views.ProductFeatureAPIView.as_view(), name='productFeature'),
    path('feature/<int:id>', views.ProductFeatureDetailsAPIView.as_view(),
         name='productFeatureDetails'),
    path('specification/', views.ProductSpecificationAPIView.as_view(),
         name='productSpecification'),
    path('specification/<int:id>', views.ProductSpecificationDetailsAPIView.as_view(),
         name='productSpecificationDetails'),
    path('productalldetails/', views.ProductDetailAPIView.as_view(),
         name='productalldetails'),
    path('api/', include(router.urls)),
    path('viewallProduct/', views.viewProductAPIView.as_view(),
         name='viewallProduct'),
    path('searchallProduct/', views.searchViewProductAPIView.as_view(),
         name='searchallProduct'),
    path('viewvendorallProduct/', views.viewVendorProductAPIView.as_view(),
         name='viewvendorallProduct'),
    path('search/', views.viewSearchVendorProductAPIView.as_view(), name='search'),
    path('viewProducts/<id>', views.SingleVendorProductAPIView.as_view(),
         name='viewProducts'),
    path('viewadminProducts/<id>',
         views.SingleProductAdminAPIView.as_view(), name='viewadminProducts'),
    path('viewuserProducts/',
         views.SingleProductUserAPIView.as_view(), name='viewuserProducts'),

    path('addproduct/', views.ProductaddAPI.as_view(), name='addproduct'),
    path('multipleproductfeature/', views.MutilpleProductFeatureAPI.as_view(),
         name='multipleproductfeature'),
    path('multipleproductsecification/', views.MutilpleProductSpecificationAPI.as_view(),
         name='multipleproductsecification'),
    path('multipleproductimage/', views.MutilpleProductImageAPI.as_view(),
         name='multipleproductimage'),
    path('inventoryProduct/', views.InventoryDetailAPIView.as_view(),
         name='inventoryProduct'),
    path('newArrival/', views.NewArrivalAPIView.as_view(), name='newArrival'),
    path('mostView/', views.MostViewAPIView.as_view(), name='mostView'),
    path('mostRatted/', views.MostRattedAPIView.as_view(), name='mostRatted'),
    path('allshop/', views.AllShopAPIView.as_view(), name='allshop'),
    path('topProduct/', views.TopProductAPIView.as_view(), name='topProduct'),
    path('AdminTopProduct/', views.AdminTopProductAPIView.as_view(),
         name='AdminTopProduct'),
    path('AdminLowestProduct/', views.AdminLowestProductAPIView.as_view(),
         name='AdminLowestProduct'),
    path('AdminTopViewProduct/', views.AdminTopViewProductAPIView.as_view(),
         name='AdminTopViewProduct'),
    path('AdminLowestViewProduct/', views.AdminLowestViewProductAPIView.as_view(),
         name='AdminLowestViewProduct'),
    path('AdminTopReviewProduct/', views.AdminTopRattingProductAPIView.as_view(),
         name='AdminTopReviewProduct'),
    path('AdminLowestReviewProduct/', views.AdminLowestRattingProductAPIView.as_view(),
         name='AdminLowestReviewProduct'),
]
