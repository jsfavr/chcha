# Generated by Django 3.1.1 on 2020-09-25 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0003_inventorytransaction_transactiondate'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorytransaction',
            name='transactionID',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
