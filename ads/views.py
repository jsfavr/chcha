from django.shortcuts import render
from rest_framework import permissions, views, status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import VideoAdsSerializer, VideoCategorySerializer, VideoKeyFieldSerializer, VideoSerializer
from .models import Ads, VideoKeyField, VideoCategory, Video
from django.core import serializers
from django.conf import settings
from product.permissions import IsOwner
from django.db.models import Avg, Max, Min, Sum
from moviepy.editor import *
from django.db.models import Q
from datetime import datetime
import random


# Create your views here.
class VideoAdsAPIView(ListCreateAPIView):
    serializer_class = VideoAdsSerializer
    queryset = Ads.objects.all()

    def perfrom_create(self, serializer):
        return serializer.save()


class VideoAdsDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = VideoAdsSerializer
    queryset = Ads.objects.all()

    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class AddVideoAds(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        inputs = request.data
        user_id = self.request.user.id
        Ads.objects.create(
            companyName=inputs['CompanyName'],
            companyLogo=inputs['companyLogo'],
            companyShortDescriptions=inputs['companyShortDescriptions'],
            domainName=inputs['domainName'],
            redirectURL=inputs['redirectURL'],
            video=inputs['video'],
            status=1,
            # videoLength=inputs['videoLength'],
            # planID=inputs['planID'],
            # transID=inputs['transID'],
            # payableAmount=inputs['amount'],

        )
        return Response({'msg': 'Video Ads add Successfully'}, status=status.HTTP_200_OK)


class ViewVideoAds(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = self.request.user.id
        print(user_id)
        adsArray = []
        path = settings.MEDIA_URL
        ads = Ads.objects.all().order_by('-id')
        for eachAds in ads:
            newArr = {
                'companyName': eachAds.companyName,
                'companyLogo': path+str(eachAds.companyLogo),
                'companyShortDescriptions': eachAds.companyShortDescriptions,
                'domainName': eachAds.domainName,
                'redirectURL': eachAds.redirectURL,
                'video': path+str(eachAds.video),
                # 'videoLength':eachAds.videoLength,
                # 'views':eachAds.views,
                'status': eachAds.status,
                # 'payableAmount':eachAds.payableAmount,
                # 'transID':eachAds.transID,
                'created_at': eachAds.created_at,
                # 'planTitle':planDetails.title,
                # 'planView':planDetails.views,
                # 'planPrice':planDetails.planPrice,
            }
            adsArray.append(newArr)
        return Response(adsArray)


class ViewAdminVideoAds(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = self.request.user.id
        print(user_id)
        adsArray = []
        path = settings.MEDIA_URL
        ads = Ads.objects.all().order_by('-id')
        for eachAds in ads:
            newArr = {
                'id': eachAds.id,
                'companyName': eachAds.companyName,
                'companyLogo': path+str(eachAds.companyLogo),
                'companyShortDescriptions': eachAds.companyShortDescriptions,
                'domainName': eachAds.domainName,
                'redirectURL': eachAds.redirectURL,
                'video': path+str(eachAds.video),
                # 'videoLength':eachAds.videoLength,
                # 'views':eachAds.views,
                'status': eachAds.status,
                # 'payableAmount':eachAds.payableAmount,
                # 'transID':eachAds.transID,
                'created_at': eachAds.created_at,
                # 'name':userDetails.name,
                # 'email':userDetails.email,
                # 'phone':userDetails.phone,
                # 'planTitle':planDetails.title,
                # 'planView':planDetails.views,
                # 'planPrice':planDetails.planPrice,


            }
            adsArray.append(newArr)
        return Response(adsArray)


class Adsmanagement(views.APIView):
    def get(self, request):
        today = datetime.now().date()
        path = settings.MEDIA_URL
        ads_details = Ads.objects.filter(status=1).first()
        ads_details_array = {
            'id': ads_details.id,
            'companyName': ads_details.companyName,
            'companyLogo': path+str(ads_details.companyLogo),
            'companyShortDescriptions': ads_details.companyShortDescriptions,
            'domainName': ads_details.domainName,
            'redirectURL': ads_details.redirectURL,
            'video': path+str(ads_details.video),
            # 'videoLength':ads_details.videoLength,
        }
        return Response(ads_details_array)

# Create your views here.


class VideoCategoryAPIView(ListCreateAPIView):
    serializer_class = VideoCategorySerializer
    queryset = VideoCategory.objects.all()

    def perfrom_create(self, serializer):
        return serializer.save()


class VideoCategoryDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = VideoCategorySerializer
    queryset = VideoCategory.objects.all()

    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()

# Create your views here.


class VideoAPIView(ListCreateAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def perfrom_create(self, serializer):
        return serializer.save()


class VideoDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


# Create your views here.
class VideoKeyFieldAPIView(ListCreateAPIView):
    serializer_class = VideoKeyFieldSerializer
    queryset = VideoKeyField.objects.all()

    def perfrom_create(self, serializer):
        return serializer.save()


class VideoKeyFieldDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = VideoKeyFieldSerializer
    queryset = VideoKeyField.objects.all()

    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class powerCategory(views.APIView):
    def get(self, request):
        catDetails = VideoCategory.objects.all()
        catArr = []
        for eachCat in catDetails:
            video = Video.objects.filter(videoCategory=eachCat.id).count()
            if video:
                hasChild = True
            else:
                hasChild = False
            newArr = {
                'catID': eachCat.id,
                'catName': eachCat.name,
                'catStatus': eachCat.status,
                'hasChild': hasChild,
            }
            catArr.append(newArr)
        return Response(catArr)


class powerVideo(views.APIView):
    def get(self, request):
        videoDetails = Video.objects.all()
        videoArr = []
        for eachVideo in videoDetails:
            cat = VideoCategory.objects.filter(
                id=eachVideo.videoCategory).first()
            video = {
                'name': eachVideo.videoName,
                'videoCategory': cat.name,
                'videoDescription': eachVideo.videoDescription,
                'video': str(eachVideo.video),
                'thumbnail': str(eachVideo.thumbnail),
                'status': eachVideo.status,
                'videoID': eachVideo.id,
                'catID': cat.id,
            }
            videoArr.append(video)
        return Response(videoArr)


class powerVideoAdd(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def put(self, request):
        inputs = request.data
        videoDetail = Video.objects.create(
            videoName=inputs["videoName"],
            videoCategory=inputs["videoCategory"],
            videoDescription=inputs["videoDescription"],
            video=inputs["video"],
            thumbnail=inputs["thumbnail"]
        )
        abc = [x.strip() for x in inputs['feature'].split('125458')][:]
        for pro in abc:
            VideoKeyField.objects.create(
                videoId=videoDetail.id, keyName=pro)
        returnArr = {
            'msg': 'Add Successful'
        }
        return Response(returnArr)


class powerVideoParticular(views.APIView):
    def get(self, request, id):
        eachVideo = Video.objects.filter(id=id).first()
        cat = VideoCategory.objects.filter(
            id=eachVideo.videoCategory).first()
        features = VideoKeyField.objects.filter(videoId=id)
        feature = []
        for eachFeatures in features:
            feaArr = {
                'name': eachFeatures.keyName
            }
            feature.append(feaArr)
        video = {
            'name': eachVideo.videoName,
            'videoCategory': cat.name,
            'videoDescription': eachVideo.videoDescription,
            'video': str(eachVideo.video),
            'thumbnail': str(eachVideo.thumbnail),
            'status': eachVideo.status,
            'videoID': eachVideo.id,
            'catID': cat.id,
            'features': feature
        }

        return Response(video)


class powerVideoCategory(views.APIView):
    def get(self, request):
        cat = VideoCategory.objects.filter(status=True)
        returnArr = []
        for eachCat in cat:
            videoDetails = Video.objects.filter(
                videoCategory=eachCat.id, status=True)
            videoArr = []
            for eachVideo in videoDetails:
                video = {
                    'name': eachVideo.videoName,
                    'videoDescription': eachVideo.videoDescription,
                    'video': str(eachVideo.video),
                    'thumbnail': str(eachVideo.thumbnail),
                    'status': eachVideo.status,
                    'videoID': eachVideo.id
                }
                videoArr.append(video)
            allArr = {
                'catID': eachCat.id,
                'catName': eachCat.name,
                'video': videoArr
            }
            if(videoDetails):
                returnArr.append(allArr)
        return Response(returnArr)
