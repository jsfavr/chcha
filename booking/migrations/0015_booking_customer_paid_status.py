# Generated by Django 3.1.14 on 2022-05-03 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0014_booking_vendor_paid_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='customer_paid_status',
            field=models.BooleanField(default=False),
        ),
    ]