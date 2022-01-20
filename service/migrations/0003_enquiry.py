# Generated by Django 3.1.5 on 2021-03-13 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0002_service_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=255, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]