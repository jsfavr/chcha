from rest_framework import serializers
from .models import Ads, Video, VideoCategory, VideoKeyField

class VideoAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = '__all__'


class VideoKeyFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoKeyField
        fields = '__all__'