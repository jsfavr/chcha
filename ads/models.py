from django.db import models
import os
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Ads(models.Model):
    companyName = models.CharField(default=0, max_length=100)
    companyLogo = models.ImageField(
        upload_to='uploads/ads/companyLogo/', null=True)
    companyShortDescriptions = models.TextField(default=0, max_length=5000)
    domainName = models.CharField(default=0, max_length=500)
    redirectURL = models.CharField(default=0, max_length=500)
    video = models.FileField(upload_to='uploads/ads/video/', null=True)
    # videoLength = models.CharField(default=0, max_length=100)
    # user_id = models.IntegerField(default=0)
    # planID=models.IntegerField(default=0)
    # views = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    # payableAmount=models.IntegerField(default=0)
    # transID = models.CharField(default=0, max_length=100)
    created_at = models.DateTimeField(auto_now=True)


class VideoCategory(models.Model):
    name = models.CharField(default=0, max_length=100)
    status = models.BooleanField(default=True)


class Video(models.Model):
    videoName = models.CharField(default=0, max_length=100)
    videoCategory = models.IntegerField(default=0)
    videoDescription = models.TextField(null=True, max_length=500)
    video = models.FileField(upload_to='uploads/powerVideo/video', default='')
    thumbnail = models.ImageField(
        upload_to='uploads/powerVideo/thumbnail', default='')
    status = models.BooleanField(default=True)


class VideoKeyField(models.Model):
    videoId = models.IntegerField(default=0)
    keyName = models.CharField(max_length=200, null=True)


@receiver(models.signals.post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)


@receiver(models.signals.pre_save, sender=Video)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Video` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Video.objects.get(pk=instance.pk).video
    except Video.DoesNotExist:
        return False

    new_file = instance.video
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    try:
        old_file = Video.objects.get(pk=instance.pk).thumbnail
    except Video.DoesNotExist:
        return False

    new_file = instance.thumbnail
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=Ads)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)
    if instance.companyLogo:
        if os.path.isfile(instance.companyLogo.path):
            os.remove(instance.companyLogo.path)


@receiver(models.signals.pre_save, sender=Ads)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Video` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Ads.objects.get(pk=instance.pk).video
    except Video.DoesNotExist:
        return False

    new_file = instance.video
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    try:
        old_file = Ads.objects.get(pk=instance.pk).companyLogo
    except Video.DoesNotExist:
        return False

    new_file = instance.companyLogo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
