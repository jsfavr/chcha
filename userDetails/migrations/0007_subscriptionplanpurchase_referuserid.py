# Generated by Django 3.1.5 on 2021-03-16 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userDetails', '0006_subscriptionplanpurchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplanpurchase',
            name='referUserID',
            field=models.IntegerField(default=0),
        ),
    ]
