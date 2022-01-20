# Generated by Django 3.1.1 on 2020-09-13 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('address', '0003_auto_20200912_1618'),
        ('product', '0005_auto_20200912_1233'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('productPrice', models.IntegerField(default=0)),
                ('productGST', models.IntegerField(default=0)),
                ('orderID', models.CharField(max_length=20)),
                ('deliveryCharge', models.IntegerField(default=0)),
                ('walletAmount', models.IntegerField(default=0)),
                ('paymentType', models.CharField(max_length=20)),
                ('orderStatus', models.IntegerField(default=1)),
                ('razorpayPaymentId', models.CharField(max_length=100)),
                ('OrderDate', models.DateField(auto_now_add=True)),
                ('deliveryDate', models.DateField(blank=True, null=True)),
                ('returnDate', models.DateField(blank=True, null=True)),
                ('orderInTransitDate', models.DateField(blank=True, null=True)),
                ('readyForReturnDate', models.DateField(blank=True, null=True)),
                ('cancelDate', models.DateField(blank=True, null=True)),
                ('deliveryBoyId', models.IntegerField(default=0)),
                ('returnBoyId', models.IntegerField(default=0)),
                ('reviewStatus', models.BooleanField(default=False)),
                ('redeemStatus', models.BooleanField(default=False)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('shippingAddressId',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.shippingaddress')),
                (
                'user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]