from django.urls import path, include
from . import views
from .views import CategoryViewSets, SubCategoryViewSets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cat',CategoryViewSets,basename='cat'),
router.register('subcat',SubCategoryViewSets,basename='subcat'),
urlpatterns = [
    path('cat/', views.CategoryAPIView.as_view(), name='category'),
    path('cat/<int:id>', views.CategoryDetailsAPIView.as_view(), name='categoryDetails'),
    path('subcat/', views.SubCategoryAPIView.as_view(), name='Subcategory'),
    path('subcat/<int:id>', views.SubCategoryDetailsAPIView.as_view(), name='SubcategoryDetails'),
    path('subsubcat/', views.SubSubCategoryAPIView.as_view(), name='SubSubcategory'),
    path('subsubcat/<int:id>', views.SubSubCategoryDetailsAPIView.as_view(), name='SubSubcategoryDetails'),
    path('viewCat', views.ViewCategoryAPIView.as_view(), name='categorgfgyy'),
    path('api/',include(router.urls)),
    path('viewCat/<int:id>', views.ViewCategoryAPIView.as_view(), name='categorgfgyy'),
    path('api/',include(router.urls)),
    path('viewsub/<id>',views.SubcatDetailsAPIView.as_view(),name='viewsub'),
    path('multiple/',views.SubcatView.as_view(),name='multiple'),
    path('topcat/',views.TopcatView.as_view(),name='topcat'),
    path('checkchild/',views.CheckchildAPI.as_view(),name='checkchild'),
    path('subcheckchild/',views.ChecksubchildAPI.as_view(),name='subcheckchild'),
    path('procheckchild/',views.CheckprochildAPI.as_view(),name='procheckchild'),
    path('getsubcat/',views.SubcategoryDetails.as_view(),name='getsubcat'),
    path('subcategories/',views.GetSubcategories.as_view(),name='subcategories'),
    path('subsubcategories/',views.GetSubSubcategories.as_view(),name='subsubcategories'),
]
