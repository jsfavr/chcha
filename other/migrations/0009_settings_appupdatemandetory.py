# Generated by Django 3.1.5 on 2021-04-24 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0008_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='appUpdateMandetory',
            field=models.BooleanField(default=False),
        ),
    ]
