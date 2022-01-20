from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CategorySerializer, SubCategorySerializer, SubSubCategorySerializer
from rest_framework import permissions,views,status
from .models import Category,SubCategory, SubSubCategory
from product.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.db import connection
from rest_framework import viewsets
from rest_framework.response import Response
import json
from product.models import Product
from booking.models import Booking
class CategoryAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class CategoryDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class SubCategoryAPIView(ListCreateAPIView):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class SubCategoryDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class SubSubCategoryAPIView(ListCreateAPIView):
    serializer_class = SubSubCategorySerializer
    queryset = SubSubCategory.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perfrom_create(self, serializer):
        return serializer.save()


class SubSubCategoryDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubSubCategorySerializer
    queryset = SubSubCategory.objects.all()
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()

class ViewCategoryAPIView(ListCreateAPIView):

    def get(self,request):
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM product_productimage")
            row = cursor.fetchall()
            return Response(row)

class CategoryViewSets(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        categories = Category.objects.all()
        return categories

class SubCategoryViewSets(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        subcategories = SubCategory.objects.all()
        return subcategories

    def create(self,request,*args,**kwargs):
        subcategories_data = request.data
        new_data = Category.objects.create(cat_name=subcategories_data['cat_details']['cat_name'])
        new_data.save()

        new_subcat = SubCategory.objects.create(sub_cat_name=subcategories_data['sub_cat_name'],sub_cat_icon=subcategories_data['sub_cat_icon'],commission=subcategories_data['commission'],gst=subcategories_data['gst'],homepage_view_status=subcategories_data['homepage_view_status'],cat_details = new_data )
        new_subcat.save()

        serializer = SubCategorySerializer(new_subcat)
        return Response(serializer.data)
class SubcatDetailsAPIView(views.APIView):
    def get(self,request,id):
        pid = id
        print(pid)
        # data = Category.objects.filter(id=pid)
        # data1 = SubCategorytype.objects.filter(cat_id_id=pid)
        # context = {'subcat':data,'cat':data1}
        # print(context)
        cursor = connection.cursor()
        cursor.execute('SELECT s.*,c.* FROM category_subcategorytype s inner join category_category c on s.cat_id_id=c.id where s.cat_id_id=3')
        row = cursor.fetchall()
        data=row
        json_output = json.dumps(data)
        # print(json_output)
        # data = SubCategorytype.objects.raw('SELECT s.*,c.* FROM category_subcategorytype s inner join category_category c on s.cat_id_id=c.id where s.cat_id_id=3')
        # query = 'SELECT * FROM category_subcategorytype WHERE id = %s' % pid
        # cursor.execute(query)
        # row = cursor.fetchall()
        # data = SubCategorytype.objects.raw(query)
        # post_list = serializers.serialize('json', data)
        # return HttpResponse(post_list, content_type="application/json")
        return Response(json_output)

class SubcatView(views.APIView):
    def post(self,request):
        datas = request.data
        new_data = Category.objects.create(cat_name=datas['cat_name'],cat_icon=datas['cat_icon'])
        new_data.save()
        cid = new_data.id
        new_subcat = SubCategory.objects.create(sub_cat_name=datas['sub_cat_name'],sub_cat_icon=datas['sub_cat_icon'],commission=datas['commission'],gst=datas['gst'],homepage_view_status=datas['homepage_view_status'],cat_id_id = cid )
        new_subcat.save()

        # print(new_data.id)
        # post_list = serializers.serialize('json', new_data)
        # return HttpResponse(post_list, content_type="application/json")
        # return Response(new_data)
        return Response({'category': 'Successfully Added'}, status=status.HTTP_200_OK)
        # return Response(datas)

class TopcatView(views.APIView):
    def get(self,request):
        booking_details=Category.objects.all()[:15]
        catarr=[]
        for cat_d in booking_details:
            catdetails = {
                    'id':cat_d.id,
                    'cat_name':cat_d.cat_name,
                    'icon':str(cat_d.cat_icon),
            }
            catarr.append(catdetails)
        return Response(catarr)

class CheckchildAPI(views.APIView):
    def post(self,request):
        inputs=request.data
        get_sub=SubCategory.objects.filter(cat_id=inputs['id'])
        if get_sub.first():
            return Response({'flag':1},status=status.HTTP_200_OK)
        else:
            return Response({'flag':0},status=status.HTTP_200_OK)

class ChecksubchildAPI(views.APIView):
    def post(self,request):
        inputs=request.data
        get_sub_sub=SubSubCategory.objects.filter(sub_cat_id=inputs['id'])
        if get_sub_sub.first():
            return Response({'flag':1},status=status.HTTP_200_OK)
        else:
            return Response({'flag':0},status=status.HTTP_200_OK)

class CheckprochildAPI(views.APIView):
    def post(self,request):
        inputs=request.data
        get_pro=Product.objects.filter(sub_sub_cat_id_id=inputs['id'])
        if get_pro.first():
            return Response({'flag':1},status=status.HTTP_200_OK)
        else:
            return Response({'flag':0},status=status.HTTP_200_OK)

class SubcategoryDetails(views.APIView):
    def post(self,request):
        inputs = request.data
        get_sub=SubCategory.objects.filter(id=inputs['id']).first()
        if get_sub:
            return Response({'gst':get_sub.gst,'commission':get_sub.commission},status=status.HTTP_200_OK)
        else:
            return Response({'msg':0},status=status.HTTP_200_OK)
