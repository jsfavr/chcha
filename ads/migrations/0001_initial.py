# Generated by Django 3.1.5 on 2021-02-17 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BannerAds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(default=0, max_length=100)),
                ('banner', models.ImageField(null=True, upload_to='uploads/ads/banner/')),
                ('redirectURL', models.CharField(default=0, max_length=500)),
                ('user_id', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoAds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(default=0, max_length=100)),
                ('companyLogo', models.ImageField(null=True, upload_to='uploads/ads/companyLogo/')),
                ('companyShortDescriptions', models.TextField(default=0, max_length=5000)),
                ('domainName', models.CharField(default=0, max_length=500)),
                ('redirectURL', models.CharField(default=0, max_length=500)),
                ('video', models.FileField(null=True, upload_to='uploads/ads/video/')),
                ('videoLength', models.CharField(default=0, max_length=100)),
                ('user_id', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
