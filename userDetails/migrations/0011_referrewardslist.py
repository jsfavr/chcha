# Generated by Django 3.1.5 on 2021-04-26 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userDetails', '0010_minimumordervalueforuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferRewardsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('register_user_id', models.IntegerField(default=0)),
                ('parent_user_id', models.IntegerField(default=0)),
                ('cashbackLevel', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
                ('cashbackStatus', models.BooleanField(default=False)),
            ],
        ),
    ]