# Generated by Django 3.1.1 on 2020-09-12 12:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('userDetails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posdetails',
            name='activeStatus',
            field=models.BooleanField(default=True),
        ),
    ]
