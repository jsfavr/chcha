# Generated by Django 3.1.5 on 2021-04-09 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_auto_20200912_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='point',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wallettransaction',
            name='walletType',
            field=models.CharField(default='MONEY', max_length=100),
        ),
    ]
