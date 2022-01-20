# Generated by Django 3.1.1 on 2020-10-07 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0007_auto_20201007_1447'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0003_auto_20201007_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='productPrice',
            new_name='productPayablePrice',
        ),
        migrations.AddField(
            model_name='booking',
            name='productSellingPrice',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='BookingPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grandTotal', models.IntegerField(default=0)),
                ('subTotal', models.IntegerField(default=0)),
                ('razorpayPaymentId', models.CharField(max_length=100)),
                ('paymentType', models.CharField(max_length=20)),
                ('deliveryCharge', models.IntegerField(default=0)),
                ('walletAmount', models.IntegerField(default=0)),
                ('couponDiscount', models.IntegerField(default=0)),
                ('couponCode', models.CharField(blank=True, max_length=20, null=True)),
                ('shippingAddressId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.shippingaddress')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]