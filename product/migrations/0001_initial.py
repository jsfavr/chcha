# Generated by Django 3.1.1 on 2020-09-12 05:00

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50)),
                ('brand_logo', models.ImageField(upload_to='uploads/brand/')),
            ],
        ),
    ]
