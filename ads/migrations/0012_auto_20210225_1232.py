# Generated by Django 3.1.5 on 2021-02-25 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0011_adsstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adsstatus',
            name='ads_id',
            field=models.IntegerField(default=0),
        ),
    ]
