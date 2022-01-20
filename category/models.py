from django.db import models


# Create your models here.
class Category(models.Model):
    cat_name = models.CharField(max_length=50)
    cat_icon = models.ImageField(upload_to='uploads/category/')


class SubCategory(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    sub_cat_name = models.CharField(max_length=20)
    sub_cat_icon = models.ImageField(upload_to='uploads/subcategory/',null=True)
    commission = models.IntegerField(default=1)
    gst = models.IntegerField(default=1)
    homepage_view_status = models.BooleanField(default=False)
   # cat_details = models.OneToOneField(Category,on_delete=models.CASCADE,null=True)

# class SubCategorytype(models.Model):
#     cat_id = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
#     sub_cat_name = models.CharField(max_length=20)
#     sub_cat_icon = models.ImageField(upload_to='uploads/subcategory/')
#     commission = models.IntegerField(default=1)
#     gst = models.IntegerField(default=1)
#     homepage_view_status = models.BooleanField(default=False)
#

class SubSubCategory(models.Model):
    sub_cat_id = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=1)
    sub_sub_cat_name = models.CharField(max_length=20)
    sub_sub_cat_icon = models.ImageField(upload_to='uploads/subsubcategory/',null=True)
