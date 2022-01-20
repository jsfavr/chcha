# Generated by Django 3.1.1 on 2020-09-12 11:07

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, null=True)),
                ('discount', models.IntegerField(default=0)),
                ('couponImage', models.ImageField(upload_to='uploads/couponImage/')),
                ('couponCode', models.CharField(max_length=100, unique=True)),
                ('couponType', models.CharField(max_length=50)),
                ('activeStatus', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DisplayBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/couponImage/')),
            ],
        ),
    ]
