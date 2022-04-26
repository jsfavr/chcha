from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import generics, status, views, viewsets
from .serializers import ProductBrandSerializer, ProductGroupSerializer, ProductFeatureSerializer, \
    ProductImageSerializer, ProductSpecificationSerializer, ProductSerializer, ProductDetailsSerializer
from rest_framework import permissions
from .models import ProductBrand, ProductGroup, ProductFeature, Product, ProductImage, ProductSpecification
from rest_framework.response import Response
from django.http import HttpResponse
from django.core import serializers
from . import models
from .permissions import IsOwner
import json
from other.models import InventoryTransaction
from category.models import Category, SubCategory, SubSubCategory
from django.http import JsonResponse
from authentication.models import User
from userDetails.models import VendorDetails
from django.db.models import Count
from other.models import Review
from booking.models import Booking
from django.db.models import Q


class ProductBrandAPIView(ListCreateAPIView):
    serializer_class = ProductBrandSerializer
    queryset = ProductBrand.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductBrandDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductBrandSerializer
    queryset = ProductBrand.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductGroupAPIView(ListCreateAPIView):
    serializer_class = ProductGroupSerializer
    queryset = ProductGroup.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductGroupDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductGroupSerializer
    queryset = ProductGroup.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perfrom_create(self, serializer):
        return serializer.save(user_id=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user)


class ProductDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductImageAPIView(ListCreateAPIView):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductImageDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductSpecificationAPIView(ListCreateAPIView):
    serializer_class = ProductSpecificationSerializer
    queryset = ProductSpecification.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductSpecificationDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSpecificationSerializer
    queryset = ProductSpecification.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductFeatureAPIView(ListCreateAPIView):
    serializer_class = ProductFeatureSerializer
    queryset = ProductFeature.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductFeatureDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductFeatureSerializer
    queryset = ProductFeature.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class ProductDetailAPIView(views.APIView):
    def get(self, request):
        data = Product.objects.all()
        post_list = serializers.serialize('json', data)
        return Response(post_list)


class InventoryDetailAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user_id = self.request.user.id
        data = Product.objects.filter(user_id_id=user_id)
        post_list = serializers.serialize('json', data)
        return Response(post_list)


class searchViewProductAPIView(views.APIView):
    def post(self, request):
        # print(request.GET)
        inputs = request.data
        if inputs['searchType'] == 'Product Name':
            product = Product.objects.filter(
                productName__icontains=inputs['searchText'])
            # print('Product Name')
        elif inputs['searchType'] == 'Product Code':
            product = Product.objects.filter(
                productCode__icontains=inputs['searchText'])
        elif inputs['searchType'] == 'Product Group':
            productGroup = ProductGroup.objects.filter(
                group_name__icontains=inputs['searchText'])
            product = []
            for eachGroup in productGroup:
                productArr = Product.objects.filter(
                    productGroupID_id=eachGroup.id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Product Brand':
            productBrand = ProductBrand.objects.filter(
                brand_name__icontains=inputs['searchText'])
            product = []
            for eachBrand in productBrand:
                productArr = Product.objects.filter(
                    productBrandID_id=eachBrand.id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Customer ID':
            vendorID = User.objects.filter(
                username__icontains=inputs['searchText'])
            product = []
            for eachVendor in vendorID:
                productArr = Product.objects.filter(
                    user_id_id=eachVendor.id)
                for eachProd in productArr:
                    product.append(eachProd)

        elif inputs['searchType'] == 'Vendor Name':
            vendorID = User.objects.filter(
                name__icontains=inputs['searchText'])
            product = []
            for eachVendor in vendorID:
                productArr = Product.objects.filter(
                    user_id_id=eachVendor.id)
                for eachProd in productArr:
                    product.append(eachProd)

        elif inputs['searchType'] == 'Vendor Email':
            vendorID = User.objects.filter(
                email__icontains=inputs['searchText'])
            product = []
            for eachVendor in vendorID:
                productArr = Product.objects.filter(
                    user_id_id=eachVendor.id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Vendor Phone':
            vendorID = User.objects.filter(
                phone__icontains=inputs['searchText'])
            product = []
            for eachVendor in vendorID:
                productArr = Product.objects.filter(
                    user_id_id=eachVendor.id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Category':
            category = Category.objects.filter(
                cat_name__icontains=inputs['searchText'])
            product = []
            for eachCategory in category:
                productArr = Product.objects.filter(
                    cat_id_id=eachCategory.id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Sub Category':
            subCategory = SubCategory.objects.filter(
                sub_cat_name__icontains=inputs['searchText'])
            product = []
            for eachCategory in subCategory:
                productArr = Product.objects.filter(
                    sub_cat_id_id=eachCategory.id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Sub Sub Category':
            subSubCategory = SubSubCategory.objects.filter(
                sub_sub_cat_name__icontains=inputs['searchText'])
            product = []
            for eachCategory in subSubCategory:
                productArr = Product.objects.filter(
                    sub_sub_cat_id_id=eachCategory.id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Vendor Status':
            product = Product.objects.filter(
                vendorActiveStatus=inputs['searchText'])
        elif inputs['searchType'] == 'Admin Status':
            product = Product.objects.filter(
                adminActiveStatus=inputs['searchText'])
        else:
            product = Product.objects.all()

        modifiedProduct = []
        for eachProd in product:
            productFirst = Product.objects.filter(id=eachProd.id).first()
            pdel = Product.objects.filter(id=productFirst.id)
            catdel = Category.objects.filter(id=productFirst.cat_id_id)
            subcatdel = SubCategory.objects.filter(
                id=productFirst.sub_cat_id_id)
            subsubcatdel = SubSubCategory.objects.filter(
                id=productFirst.sub_sub_cat_id_id)
            image1 = ProductImage.objects.filter(productID_id=productFirst.id)
            feature = ProductFeature.objects.filter(
                productID_id=productFirst.id)
            specification = ProductSpecification.objects.filter(
                productID_id=productFirst.id)
            brand = ProductBrand.objects.filter(
                id=productFirst.productBrandID_id)
            group = ProductGroup.objects.filter(
                id=productFirst.productGroupID_id)
            vendor = User.objects.filter(id=productFirst.user_id_id)

            product_list = serializers.serialize('json', pdel)
            cat_list = serializers.serialize('json', catdel)
            subcat_list = serializers.serialize('json', subcatdel)
            subsubcat_list = serializers.serialize('json', subsubcatdel)
            image_list = serializers.serialize('json', image1)
            feature_list = serializers.serialize('json', feature)
            specification_list = serializers.serialize('json', specification)
            brand_name = serializers.serialize('json', brand)
            group_name = serializers.serialize('json', group)
            vendorDetails = serializers.serialize('json', vendor)
            newProd = {
                'details': product_list,
                'cat_details': cat_list,
                'subcat_details': subcat_list,
                'subsubcat_details': subsubcat_list,
                'image': image_list,
                'feature': feature_list,
                'specification': specification_list,
                'brand': brand_name,
                'group': group_name,
                'vendorDetails': vendorDetails
            }
            # print(newProd)
            modifiedProduct.append(newProd)
            # print(modifiedProduct)
        # data = json.loads(modifiedProduct)
        # print(modifiedProduct)
        return Response(modifiedProduct)
        # post_list = serializers.serialize('json', modifiedProduct)
        # return HttpResponse(post_list, content_type="application/json")


class viewProductAPIView(views.APIView):
    def get(self, request):
        # print(request.GET)
        image = ProductImage.objects.all()
        product = Product.objects.all()
        modifiedProduct = []
        for eachProd in product:
            pdel = Product.objects.filter(id=eachProd.id)
            catdel = Category.objects.filter(id=eachProd.cat_id_id)
            subcatdel = SubCategory.objects.filter(id=eachProd.sub_cat_id_id)
            subsubcatdel = SubSubCategory.objects.filter(
                id=eachProd.sub_sub_cat_id_id)
            image1 = ProductImage.objects.filter(productID_id=eachProd.id)
            feature = ProductFeature.objects.filter(productID_id=eachProd.id)
            specification = ProductSpecification.objects.filter(
                productID_id=eachProd.id)
            brand = ProductBrand.objects.filter(id=eachProd.productBrandID_id)
            group = ProductGroup.objects.filter(id=eachProd.productGroupID_id)
            vendor = User.objects.filter(id=eachProd.user_id_id)

            product_list = serializers.serialize('json', pdel)
            cat_list = serializers.serialize('json', catdel)
            subcat_list = serializers.serialize('json', subcatdel)
            subsubcat_list = serializers.serialize('json', subsubcatdel)
            image_list = serializers.serialize('json', image1)
            feature_list = serializers.serialize('json', feature)
            specification_list = serializers.serialize('json', specification)
            brand_name = serializers.serialize('json', brand)
            group_name = serializers.serialize('json', group)
            vendorDetails = serializers.serialize('json', vendor)
            newProd = {
                'details': product_list,
                'cat_details': cat_list,
                'subcat_details': subcat_list,
                'subsubcat_details': subsubcat_list,
                'image': image_list,
                'feature': feature_list,
                'specification': specification_list,
                'brand': brand_name,
                'group': group_name,
                'vendorDetails': vendorDetails
            }
            # print(newProd)
            modifiedProduct.append(newProd)
            # print(modifiedProduct)
        # data = json.loads(modifiedProduct)
        # print(modifiedProduct)
        return Response(modifiedProduct)
        # post_list = serializers.serialize('json', modifiedProduct)
        # return HttpResponse(post_list, content_type="application/json")


class viewVendorProductAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        # print(request.GET)
        user_id = self.request.user.id
        image = ProductImage.objects.all()
        product = Product.objects.filter(user_id_id=user_id)
        modifiedProduct = []
        for eachProd in product:
            pdel = Product.objects.filter(id=eachProd.id)
            catdel = Category.objects.filter(id=eachProd.cat_id_id)
            subcatdel = SubCategory.objects.filter(id=eachProd.sub_cat_id_id)
            subsubcatdel = SubSubCategory.objects.filter(
                id=eachProd.sub_sub_cat_id_id)
            image1 = ProductImage.objects.filter(productID_id=eachProd.id)
            feature = ProductFeature.objects.filter(productID_id=eachProd.id)
            specification = ProductSpecification.objects.filter(
                productID_id=eachProd.id)
            brand = ProductBrand.objects.filter(id=eachProd.productBrandID_id)
            group = ProductGroup.objects.filter(id=eachProd.productGroupID_id)
            product_list = serializers.serialize('json', pdel)
            cat_list = serializers.serialize('json', catdel)
            subcat_list = serializers.serialize('json', subcatdel)
            subsubcat_list = serializers.serialize('json', subsubcatdel)
            image_list = serializers.serialize('json', image1)
            feature_list = serializers.serialize('json', feature)
            specification_list = serializers.serialize('json', specification)
            brand_name = serializers.serialize('json', brand)
            group_name = serializers.serialize('json', group)
            newProd = {
                'details': product_list,
                'cat_details': cat_list,
                'subcat_details': subcat_list,
                'subsubcat_details': subsubcat_list,
                'image': image_list,
                'feature': feature_list,
                'specification': specification_list,
                'brand': brand_name,
                'group': group_name,
            }
            # print(newProd)
            modifiedProduct.append(newProd)
            # print(modifiedProduct)
        # data = json.loads(modifiedProduct)
        # print(modifiedProduct)
        return Response(modifiedProduct)
        # post_list = serializers.serialize('json', modifiedProduct)
        # return HttpResponse(post_list, content_type="application/json")


class viewSearchVendorProductAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        # print(request.GET)
        user_id = self.request.user.id
        inputs = request.data
        if inputs['searchType'] == 'Product Name':
            product = Product.objects.filter(
                productName__icontains=inputs['searchText'], user_id_id=user_id)
            # print('Product Name')
        elif inputs['searchType'] == 'Product Code':
            product = Product.objects.filter(
                productCode__icontains=inputs['searchText'], user_id_id=user_id)
        elif inputs['searchType'] == 'Product Group':
            productGroup = ProductGroup.objects.filter(
                group_name__icontains=inputs['searchText'])
            product = []
            for eachGroup in productGroup:
                productArr = Product.objects.filter(
                    productGroupID_id=eachGroup.id, user_id_id=user_id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Product Brand':
            productBrand = ProductBrand.objects.filter(
                brand_name__icontains=inputs['searchText'])
            product = []
            for eachBrand in productBrand:
                productArr = Product.objects.filter(
                    productBrandID_id=eachBrand.id, user_id_id=user_id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Customer ID':
            vendorID = User.objects.filter(
                username__icontains=inputs['searchText'])
            product = []
            for eachVendor in vendorID:
                productArr = Product.objects.filter(
                    user_id_id=eachVendor.id)
                for eachProd in productArr:
                    product.append(eachProd)

        elif inputs['searchType'] == 'Vendor Name':
            vendorID = User.objects.filter(
                name__icontains=inputs['searchText'])
            product = []
            for eachVendor in vendorID:
                productArr = Product.objects.filter(
                    user_id_id=eachVendor.id)
                for eachProd in productArr:
                    product.append(eachProd)

        elif inputs['searchType'] == 'Vendor Email':
            vendorID = User.objects.filter(
                email__icontains=inputs['searchText'])
            product = []
            for eachVendor in vendorID:
                productArr = Product.objects.filter(
                    user_id_id=eachVendor.id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Vendor Phone':
            vendorID = User.objects.filter(
                phone__icontains=inputs['searchText'])
            product = []
            for eachVendor in vendorID:
                productArr = Product.objects.filter(
                    user_id_id=eachVendor.id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Category':
            category = Category.objects.filter(
                cat_name__icontains=inputs['searchText'])
            product = []
            for eachCategory in category:
                productArr = Product.objects.filter(
                    cat_id_id=eachCategory.id, user_id_id=user_id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Sub Category':
            subCategory = SubCategory.objects.filter(
                sub_cat_name__icontains=inputs['searchText'])
            product = []
            for eachCategory in subCategory:
                productArr = Product.objects.filter(
                    sub_cat_id_id=eachCategory.id, user_id_id=user_id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Sub Sub Category':
            subSubCategory = SubSubCategory.objects.filter(
                sub_sub_cat_name__icontains=inputs['searchText'])
            product = []
            for eachCategory in subSubCategory:
                productArr = Product.objects.filter(
                    sub_sub_cat_id_id=eachCategory.id, user_id_id=user_id)
                for eachProd in productArr:
                    product.append(eachProd)
        elif inputs['searchType'] == 'Vendor Status':
            product = Product.objects.filter(
                vendorActiveStatus=inputs['searchText'], user_id_id=user_id)
        elif inputs['searchType'] == 'Admin Status':
            product = Product.objects.filter(
                adminActiveStatus=inputs['searchText'], user_id_id=user_id)
        else:
            product = Product.objects.filter(user_id_id=user_id)

        modifiedProduct = []
        for eachProd in product:
            productFirst = Product.objects.filter(id=eachProd.id).first()
            pdel = Product.objects.filter(id=productFirst.id)
            catdel = Category.objects.filter(id=productFirst.cat_id_id)
            subcatdel = SubCategory.objects.filter(
                id=productFirst.sub_cat_id_id)
            subsubcatdel = SubSubCategory.objects.filter(
                id=productFirst.sub_sub_cat_id_id)
            image1 = ProductImage.objects.filter(
                productID_id=productFirst.id)
            feature = ProductFeature.objects.filter(
                productID_id=productFirst.id)
            specification = ProductSpecification.objects.filter(
                productID_id=productFirst.id)
            brand = ProductBrand.objects.filter(
                id=productFirst.productBrandID_id)
            group = ProductGroup.objects.filter(
                id=productFirst.productGroupID_id)
            vendor = User.objects.filter(id=productFirst.user_id_id)

            product_list = serializers.serialize('json', pdel)
            cat_list = serializers.serialize('json', catdel)
            subcat_list = serializers.serialize('json', subcatdel)
            subsubcat_list = serializers.serialize('json', subsubcatdel)
            image_list = serializers.serialize('json', image1)
            feature_list = serializers.serialize('json', feature)
            specification_list = serializers.serialize(
                'json', specification)
            brand_name = serializers.serialize('json', brand)
            group_name = serializers.serialize('json', group)
            vendorDetails = serializers.serialize('json', vendor)
            newProd = {
                'details': product_list,
                'cat_details': cat_list,
                'subcat_details': subcat_list,
                'subsubcat_details': subsubcat_list,
                'image': image_list,
                'feature': feature_list,
                'specification': specification_list,
                'brand': brand_name,
                'group': group_name,
                'vendorDetails': vendorDetails
            }
            # print(newProd)
            modifiedProduct.append(newProd)
            # print(modifiedProduct)
        # data = json.loads(modifiedProduct)
        # print(modifiedProduct)
        return Response(modifiedProduct)
        # post_list = serializers.serialize('json', modifiedProduct)
        # return HttpResponse(post_list, content_type="application/json")


class SingleProductAdminAPIView(views.APIView):
    def get(self, request, id):
        # print(request.GET)
        pid = id
        image = ProductImage.objects.all()
        product = Product.objects.filter(id=pid)
        modifiedProduct = []
        for eachProd in product:
            pdel = Product.objects.filter(id=eachProd.id)
            catdel = Category.objects.filter(id=eachProd.cat_id_id)
            subcatdel = SubCategory.objects.filter(id=eachProd.sub_cat_id_id)
            subsubcatdel = SubSubCategory.objects.filter(
                id=eachProd.sub_sub_cat_id_id)
            image1 = ProductImage.objects.filter(productID_id=eachProd.id)
            feature = ProductFeature.objects.filter(productID_id=eachProd.id)
            specification = ProductSpecification.objects.filter(
                productID_id=eachProd.id)
            brand = ProductBrand.objects.filter(id=eachProd.productBrandID_id)
            group = ProductGroup.objects.filter(id=eachProd.productGroupID_id)
            product_list = serializers.serialize('json', pdel)
            cat_list = serializers.serialize('json', catdel)
            subcat_list = serializers.serialize('json', subcatdel)
            subsubcat_list = serializers.serialize('json', subsubcatdel)
            image_list = serializers.serialize('json', image1)
            feature_list = serializers.serialize('json', feature)
            specification_list = serializers.serialize('json', specification)
            brand_name = serializers.serialize('json', brand)
            group_name = serializers.serialize('json', group)
            newProd = {
                'details': product_list,
                'cat_details': cat_list,
                'subcat_details': subcat_list,
                'subsubcat_details': subsubcat_list,
                'image': image_list,
                'feature': feature_list,
                'specification': specification_list,
                'brand': brand_name,
                'group': group_name,
            }
            # print(newProd)
            modifiedProduct.append(newProd)
            # print(modifiedProduct)
        # data = json.loads(modifiedProduct)
        # print(modifiedProduct)
        return Response(modifiedProduct)
        # post_list = serializers.serialize('json', modifiedProduct)
        # return HttpResponse(post_list, content_type="application/json")


class SingleVendorProductAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, id):
        # print(request.GET)
        pid = id
        user_id = self.request.user.id
        image = ProductImage.objects.all()
        product = Product.objects.filter(
            id=pid, user_id_id=user_id)
        modifiedProduct = []
        for eachProd in product:
            pdel = Product.objects.filter(id=eachProd.id)
            catdel = Category.objects.filter(id=eachProd.cat_id_id)
            subcatdel = SubCategory.objects.filter(id=eachProd.sub_cat_id_id)
            subsubcatdel = SubSubCategory.objects.filter(
                id=eachProd.sub_sub_cat_id_id)
            image1 = ProductImage.objects.filter(productID_id=eachProd.id)
            feature = ProductFeature.objects.filter(productID_id=eachProd.id)
            specification = ProductSpecification.objects.filter(
                productID_id=eachProd.id)
            brand = ProductBrand.objects.filter(id=eachProd.productBrandID_id)
            group = ProductGroup.objects.filter(id=eachProd.productGroupID_id)
            product_list = serializers.serialize('json', pdel)
            cat_list = serializers.serialize('json', catdel)
            subcat_list = serializers.serialize('json', subcatdel)
            subsubcat_list = serializers.serialize('json', subsubcatdel)
            image_list = serializers.serialize('json', image1)
            feature_list = serializers.serialize('json', feature)
            specification_list = serializers.serialize('json', specification)
            brand_name = serializers.serialize('json', brand)
            group_name = serializers.serialize('json', group)
            newProd = {
                'details': product_list,
                'cat_details': cat_list,
                'subcat_details': subcat_list,
                'subsubcat_details': subsubcat_list,
                'image': image_list,
                'feature': feature_list,
                'specification': specification_list,
                'brand': brand_name,
                'group': group_name,
            }
            # print(newProd)
            modifiedProduct.append(newProd)
            # print(modifiedProduct)
        # data = json.loads(modifiedProduct)
        # print(modifiedProduct)
        return Response(modifiedProduct)
        # post_list = serializers.serialize('json', modifiedProduct)
        # return HttpResponse(post_list, content_type="application/json")


class ProductaddAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        inputs = request.data
        user_id = self.request.user.id
        product_data = Product.objects.create(productCode=inputs['productCode'], skuCode=inputs['skuCode'], productName=inputs['productName'], size=inputs['size'], color=inputs['color'], mrp=inputs['mrp'], sellingPrice=inputs['sellingPrice'], totalStock=inputs['totalStock'], availableStock=inputs['availableStock'],
                                              cat_id_id=inputs['cat_id_id'], productBrandID_id=inputs['productBrandID_id'], productGroupID_id=inputs['productGroupID_id'], sub_cat_id_id=inputs['sub_cat_id_id'], sub_sub_cat_id_id=inputs['sub_sub_cat_id_id'], user_id_id=user_id, productDescription=inputs['productDescription'], contryOfOrigin=inputs['contryOfOrigin'],wihoutgstprice=inputs['wihoutgstprice'])
        product_data.save()
        pid = product_data.id
        product_image_data = ProductImage.objects.create(
            productID_id=pid, productImage=inputs['productImage'])
        product_image_data.save()

        abc = [x.strip() for x in inputs['feature'].split('125458')][:]
        for pro in abc:
            product_feature_data = ProductFeature.objects.create(
                productID_id=pid, feature=pro)
            product_feature_data.save()

        abcde = json.loads(inputs['details'])
        for pro1 in abcde:
            product_specification_data = ProductSpecification.objects.create(
                productID_id=pid, title=pro1['title'], details=pro1['details'])
            product_specification_data.save()
        quantity = product_data.totalStock
        afterTransactionQuantity = product_data.totalStock
        remarks = 'INITIAL ADD'
        transactionType = 'CREDIT'
        product_inventory_data = InventoryTransaction.objects.create(
            product_id_id=pid, quantity=quantity, afterTransactionQuantity=afterTransactionQuantity, remarks=remarks, transactionType=transactionType)
        product_inventory_data.save()
        return Response({'product': 'Successfully Added'}, status=status.HTTP_200_OK)


class MutilpleProductFeatureAPI(views.APIView):
    def post(self, request):
        inputs = request.data
        abc = [x.strip() for x in inputs['feature'].split('125458')][:]
        print(inputs['feature'])
        for pro in abc:
            product_feature_data = ProductFeature.objects.create(
                productID_id=inputs['productID_id'], feature=pro)
            product_feature_data.save()
        return Response({'product_feature': 'Successfully Added'}, status=status.HTTP_200_OK)


class MutilpleProductSpecificationAPI(views.APIView):
    def post(self, request):
        inputs = request.data
        abcde = json.loads(inputs['details'])
        for pro in abcde:
            product_specification_data = ProductSpecification.objects.create(
                productID_id=inputs['productID_id'], title=pro['title'], details=pro['details'])
            product_specification_data.save()
        return Response({'product_specification': 'Successfully Added'}, status=status.HTTP_200_OK)


class MutilpleProductImageAPI(views.APIView):
    def post(self, request):
        inputs = request.data
        product_image_data = ProductImage.objects.create(
            productID_id=inputs['productID_id'], productImage=inputs['image'])
        product_image_data.save()
        return Response({'product_image': 'Successfully Added'}, status=status.HTTP_200_OK)


class SingleProductUserAPIView(views.APIView):
    def post(self, request):
        # print(request.GET)
        # print(id)
        # product=int(id)
        # print(product)
        inputs = request.data
        if inputs['id'] or inputs['id'] != 0:
            pid = inputs['id']
        else:
            return Response({'product': 'product not found'}, status=status.HTTP_400_BAD_REQUEST)
        # print(id)
        # print(size)
        # print(color)
        # print(group)

        image = ProductImage.objects.all()
        product = Product.objects.filter(id=pid)
        modifiedProduct = []

        for eachProd in product:
            pdel = Product.objects.filter(id=eachProd.id)
            catdel = Category.objects.filter(id=eachProd.cat_id_id)
            subcatdel = SubCategory.objects.filter(id=eachProd.sub_cat_id_id)
            subsubcatdel = SubSubCategory.objects.filter(
                id=eachProd.sub_sub_cat_id_id)
            image1 = ProductImage.objects.filter(productID_id=eachProd.id)
            feature = ProductFeature.objects.filter(productID_id=eachProd.id)
            specification = ProductSpecification.objects.filter(
                productID_id=eachProd.id)
            brand = ProductBrand.objects.filter(id=eachProd.productBrandID_id)
            group = ProductGroup.objects.filter(id=eachProd.productGroupID_id)
            vendor = User.objects.filter(id=eachProd.user_id_id)
            vendor1 = VendorDetails.objects.filter(
                user_id_id=eachProd.user_id_id)
            size = Product.objects.filter(productGroupID_id=eachProd.productGroupID_id,
                                          adminActiveStatus=1, vendorActiveStatus=1, color=eachProd.color)
            color1 = Product.objects.filter(
                productGroupID_id=eachProd.productGroupID_id, adminActiveStatus=1, vendorActiveStatus=1, size=eachProd.size)
            viewCount = eachProd.viewCount
            Product.objects.filter(id=eachProd.id).update(
                viewCount=viewCount+1)
            modifiedColor = []
            for eachcolor in color1:
                det = Product.objects.filter(id=eachcolor.id)
                image122 = ProductImage.objects.filter(
                    productID_id=eachcolor.id)

                colorDetails = serializers.serialize('json', det)
                colorImage = serializers.serialize('json', image122)

                newcolor = {
                    'color': colorDetails,
                    'image': colorImage,
                }
                modifiedColor.append(newcolor)

            rel = Product.objects.filter(
                sub_sub_cat_id_id=eachProd.sub_sub_cat_id_id)
            modifiedrel = []
            for eachrel in rel:
                det = Product.objects.filter(id=eachrel.id)
                image122 = ProductImage.objects.filter(productID_id=eachrel.id)
                brandddd = ProductBrand.objects.filter(
                    id=eachrel.productBrandID_id)
                subcatdel = SubCategory.objects.filter(
                    id=eachrel.sub_cat_id_id)

                relDetails = serializers.serialize('json', det)
                relImage = serializers.serialize('json', image122)
                relbrand = serializers.serialize('json', brandddd)
                relsub = serializers.serialize('json', subcatdel)

                newrel = {
                    'rel': relDetails,
                    'image': relImage,
                    'brand': relbrand,
                    'sub': relsub

                }
                modifiedrel.append(newrel)

            ratting = []
            review1111 = Review.objects.filter(
                product_id_id=eachProd.id, status=1).order_by('-ratting')[:10]
            for eachrate in review1111:
                reviewDetails = Review.objects.filter(id=eachrate.id)
                userRateDetails = User.objects.filter(id=eachrate.user_id_id)

                reviewDetails1 = serializers.serialize('json', reviewDetails)
                userRateDetails1 = serializers.serialize(
                    'json', userRateDetails)
                newrel22 = {
                    'ratting': reviewDetails1,
                    'user': userRateDetails1,
                }
                ratting.append(newrel22)

            review5 = Review.objects.filter(
                product_id_id=eachProd.id, ratting=5)
            review4 = Review.objects.filter(
                product_id_id=eachProd.id, ratting=4)
            review3 = Review.objects.filter(
                product_id_id=eachProd.id, ratting=3)
            review2 = Review.objects.filter(
                product_id_id=eachProd.id, ratting=2)
            review1 = Review.objects.filter(
                product_id_id=eachProd.id, ratting=1)

            rev = {
                'star5': len(review5),
                'star4': len(review4),
                'star3': len(review3),
                'star2': len(review2),
                'star1': len(review1)
            }

            product_list = serializers.serialize('json', pdel)
            cat_list = serializers.serialize('json', catdel)
            subcat_list = serializers.serialize('json', subcatdel)
            subsubcat_list = serializers.serialize('json', subsubcatdel)
            image_list = serializers.serialize('json', image1)
            feature_list = serializers.serialize('json', feature)
            specification_list = serializers.serialize('json', specification)
            brand_name = serializers.serialize('json', brand)
            group_name = serializers.serialize('json', group)
            vendorDetails = serializers.serialize('json', vendor)
            vendorDetails1 = serializers.serialize('json', vendor1)
            size = serializers.serialize('json', size)

            # rel = serializers.serialize('json', rel)

            # color = serializers.serialize('json', newcolor)

            newProd = {
                'details': product_list,
                'cat_details': cat_list,
                'subcat_details': subcat_list,
                'subsubcat_details': subsubcat_list,
                'image': image_list,
                'feature': feature_list,
                'specification': specification_list,
                'brand': brand_name,
                'group': group_name,
                'vendor': vendorDetails,
                'vendorDetails': vendorDetails1,
                'size': size,
                'color': modifiedColor,
                'review': ratting,
                'rev': rev,
                'relatedProduct': modifiedrel,




            }
            # print(newProd)
            modifiedProduct.append(newProd)
            # print(modifiedProduct)
        # data = json.loads(modifiedProduct)
        # print(modifiedProduct)
        return Response(modifiedProduct)
        # post_list = serializers.serialize('json', modifiedProduct)
        # return HttpResponse(post_list, content_type="application/json")


class NewArrivalAPIView(views.APIView):
    def get(self, request):
        product = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1).order_by('-id')[:8]
        modifiedrel = []
        for eachrel in product:
            det = Product.objects.filter(id=eachrel.id)
            image122 = ProductImage.objects.filter(productID_id=eachrel.id)
            brandddd = ProductBrand.objects.filter(
                id=eachrel.productBrandID_id)
            subcatdel = SubCategory.objects.filter(id=eachrel.sub_cat_id_id)

            relDetails = serializers.serialize('json', det)
            relImage = serializers.serialize('json', image122)
            relbrand = serializers.serialize('json', brandddd)
            relsub = serializers.serialize('json', subcatdel)
            newrel = {
                'rel': relDetails,
                'image': relImage,
                'brand': relbrand,
                'sub': relsub

            }
            modifiedrel.append(newrel)
        return Response(modifiedrel)


class AllShopAPIView(views.APIView):
    def get(self, request):
        product = Product.objects.all()
        modifiedrel = []
        for eachrel in product:
            det = Product.objects.filter(id=eachrel.id)
            image122 = ProductImage.objects.filter(productID_id=eachrel.id)
            brandddd = ProductBrand.objects.filter(
                id=eachrel.productBrandID_id)
            brand = ProductBrand.objects.values('brand_name').annotate(
                dcount=Count('brand_name')).filter(id=eachrel.productBrandID_id)
            subcatdel = SubCategory.objects.filter(id=eachrel.sub_cat_id_id)
            relDetails = serializers.serialize('json', det)
            relImage = serializers.serialize('json', image122)
            relbrand = serializers.serialize('json', brandddd)
            # pband = serializers.serialize('json', brand)
            print(brand)
            relsub = serializers.serialize('json', subcatdel)
            newrel = {
                'rel': relDetails,
                'image': relImage,
                'brand': relbrand,
                'sub': relsub,
                'pband': brand
            }
            modifiedrel.append(newrel)
        return Response(modifiedrel)


class MostViewAPIView(views.APIView):
    def get(self, request):
        product = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1).order_by('-viewCount')[:8]
        modifiedrel = []
        for eachrel in product:
            det = Product.objects.filter(id=eachrel.id)
            image122 = ProductImage.objects.filter(productID_id=eachrel.id)
            brandddd = ProductBrand.objects.filter(
                id=eachrel.productBrandID_id)
            subcatdel = SubCategory.objects.filter(id=eachrel.sub_cat_id_id)

            relDetails = serializers.serialize('json', det)
            relImage = serializers.serialize('json', image122)
            relbrand = serializers.serialize('json', brandddd)
            relsub = serializers.serialize('json', subcatdel)
            newrel = {
                'rel': relDetails,
                'image': relImage,
                'brand': relbrand,
                'sub': relsub

            }
            modifiedrel.append(newrel)
        return Response(modifiedrel)


class MostRattedAPIView(views.APIView):
    def get(self, request):
        product = Product.objects.all().order_by('-avgReview')[:8]
        modifiedrel = []
        for eachrel in product:
            det = Product.objects.filter(id=eachrel.id)
            image122 = ProductImage.objects.filter(productID_id=eachrel.id)
            brandddd = ProductBrand.objects.filter(
                id=eachrel.productBrandID_id)
            subcatdel = SubCategory.objects.filter(id=eachrel.sub_cat_id_id)

            relDetails = serializers.serialize('json', det)
            relImage = serializers.serialize('json', image122)
            relbrand = serializers.serialize('json', brandddd)
            relsub = serializers.serialize('json', subcatdel)
            newrel = {
                'rel': relDetails,
                'image': relImage,
                'brand': relbrand,
                'sub': relsub

            }
            modifiedrel.append(newrel)
        return Response(modifiedrel)
# top_users = User.objects.filter(problem_user=False) \
#                 .annotate(num_submissions=Count('submission')) \
#                 .order_by('-num_submissions')[:3]


class TopProductAPIView(views.APIView):
    def get(self, request):
        booking = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1).order_by('-orderCount')[:8]
        modifiedrel = []
        for book in booking:
            product = Product.objects.filter(id=book.id)[:8]
            for eachrel in product:
                det = Product.objects.filter(id=eachrel.id)
                image122 = ProductImage.objects.filter(productID_id=eachrel.id)
                brandddd = ProductBrand.objects.filter(
                    id=eachrel.productBrandID_id)
                subcatdel = SubCategory.objects.filter(
                    id=eachrel.sub_cat_id_id)

                relDetails = serializers.serialize('json', det)
                relImage = serializers.serialize('json', image122)
                relbrand = serializers.serialize('json', brandddd)
                relsub = serializers.serialize('json', subcatdel)
                newrel = {
                    'rel': relDetails,
                    'image': relImage,
                    'brand': relbrand,
                    'sub': relsub

                }
                modifiedrel.append(newrel)
        return Response(modifiedrel)


class AdminTopProductAPIView(views.APIView):
    def get(self, request):
        booking = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1).order_by('-orderCount')[:50]
        modifiedrel = []
        for book in booking:
            product = Product.objects.filter(id=book.id)[:13]
            for eachrel in product:
                det = Booking.objects.filter(product_id_id=eachrel.id).count()
                newrel = {
                    'name': eachrel.productName,
                    'code': eachrel.productCode,
                    'id': eachrel.id,
                    'count': eachrel.orderCount

                }
                modifiedrel.append(newrel)
        return Response(modifiedrel)


class AdminLowestProductAPIView(views.APIView):
    def get(self, request):
        booking = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1).order_by('orderCount')[:100]
        modifiedrel = []
        for book in booking:
            product = Product.objects.filter(id=book.id)[:13]
            for eachrel in product:
                det = Booking.objects.filter(product_id_id=eachrel.id).count()
                newrel = {
                    'name': eachrel.productName,
                    'code': eachrel.productCode,
                    'id': eachrel.id,
                    'count': eachrel.orderCount

                }
                modifiedrel.append(newrel)
        return Response(modifiedrel)


class AdminTopViewProductAPIView(views.APIView):
    def get(self, request):
        booking = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1).order_by('-viewCount')[:100]
        modifiedrel = []
        for book in booking:
            product = Product.objects.filter(id=book.id)[:13]
            for eachrel in product:
                det = Booking.objects.filter(product_id_id=eachrel.id).count()
                newrel = {
                    'name': eachrel.productName,
                    'code': eachrel.productCode,
                    'id': eachrel.id,
                    'count': eachrel.viewCount

                }
                modifiedrel.append(newrel)
        return Response(modifiedrel)


class AdminLowestViewProductAPIView(views.APIView):
    def get(self, request):
        booking = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1).order_by('viewCount')[:100]
        modifiedrel = []
        for book in booking:
            product = Product.objects.filter(id=book.id)[:13]
            for eachrel in product:
                det = Booking.objects.filter(product_id_id=eachrel.id).count()
                newrel = {
                    'name': eachrel.productName,
                    'code': eachrel.productCode,
                    'id': eachrel.id,
                    'count': eachrel.viewCount

                }
                modifiedrel.append(newrel)
        return Response(modifiedrel)


class AdminTopRattingProductAPIView(views.APIView):
    def get(self, request):
        booking = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1).order_by('-avgReview')[:100]
        modifiedrel = []
        for book in booking:
            product = Product.objects.filter(id=book.id)[:13]
            for eachrel in product:
                det = Booking.objects.filter(product_id_id=eachrel.id).count()
                newrel = {
                    'name': eachrel.productName,
                    'code': eachrel.productCode,
                    'id': eachrel.id,
                    'count': eachrel.avgReview

                }
                modifiedrel.append(newrel)
        return Response(modifiedrel)


class AdminLowestRattingProductAPIView(views.APIView):
    def get(self, request):
        booking = Product.objects.filter(
            adminActiveStatus=1, vendorActiveStatus=1).order_by('avgReview')[:100]
        modifiedrel = []
        for book in booking:
            product = Product.objects.filter(id=book.id)[:13]
            for eachrel in product:
                det = Booking.objects.filter(product_id_id=eachrel.id).count()
                newrel = {
                    'name': eachrel.productName,
                    'code': eachrel.productCode,
                    'id': eachrel.id,
                    'count': eachrel.avgReview

                }
                modifiedrel.append(newrel)
        return Response(modifiedrel)
