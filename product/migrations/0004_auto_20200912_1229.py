# Generated by Django 3.1.1 on 2020-09-12 06:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0003_product_productfeature_productimage_productspecification'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='productDescription',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='productName',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
    ]