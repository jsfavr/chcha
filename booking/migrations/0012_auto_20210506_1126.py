# Generated by Django 3.1.5 on 2021-05-06 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_auto_20210505_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='deliveryBoyId',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='booking',
            name='returnBoyId',
            field=models.IntegerField(default=1),
        ),
    ]
