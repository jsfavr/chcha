# Generated by Django 3.1.1 on 2020-10-07 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='couponCode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='couponDiscount',
            field=models.IntegerField(default=0),
        ),
    ]
