# Generated by Django 3.1.1 on 2020-09-10 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('category', '0003_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_sub_cat_name', models.CharField(max_length=20)),
                ('sub_sub_cat_icon', models.ImageField(upload_to='uploads/subsubcategory/')),
                ('sub_cat_id',
                 models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='category.subcategory')),
            ],
        ),
    ]
