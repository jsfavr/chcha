# Generated by Django 3.1.5 on 2021-04-21 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_wallet_totalpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='walletwithdraw',
            name='transID',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='walletwithdraw',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]