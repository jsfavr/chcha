# Generated by Django 3.1.5 on 2021-02-18 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0006_auto_20210217_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerads',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='videoads',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
