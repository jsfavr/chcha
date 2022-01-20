# Generated by Django 3.1.2 on 2020-11-05 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0004_coupon_minprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/promotionBanner/')),
                ('url', models.CharField(max_length=300, null=True)),
            ],
        ),
    ]