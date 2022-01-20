# Generated by Django 3.1.5 on 2021-04-24 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0007_notifyme'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.BooleanField(default=False)),
                ('debug', models.BooleanField(default=False)),
                ('underMantanance', models.BooleanField(default=False)),
                ('livePaymentGateway', models.BooleanField(default=False)),
                ('vendorRegistration', models.BooleanField(default=True)),
            ],
        ),
    ]
