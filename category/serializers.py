from rest_framework import serializers
from .models import Category, SubCategory, SubSubCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','cat_name', 'cat_icon']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class SubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ['id','sub_cat_id', 'sub_sub_cat_name', 'sub_sub_cat_icon']
