# Generated by Django 3.1.5 on 2021-03-15 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20210315_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscriptionPrice',
        ),
    ]