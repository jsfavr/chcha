# Generated by Django 3.1.5 on 2021-03-23 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userDetails', '0007_subscriptionplanpurchase_referuserid'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplanpurchase',
            name='videoStatus',
            field=models.BooleanField(default=False),
        ),
    ]