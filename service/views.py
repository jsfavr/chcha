from authentication.models import User
from django.shortcuts import render
from .serializers import ServiceSerializer,EnquirySerializer
from . models import Service,Enquiry
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, views
from rest_framework.response import Response
from product.permissions import IsOwner
from rest_framework import permissions, status
from authentication.models import User
# Create your views here.
class ServiceAPIView(ListCreateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def perfrom_create(self, serializer):
        return serializer.save()


class ServiceAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class viewAllServiceAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        user_id=self.request.user.id
        service=[]
        are=Service.objects.filter(user_id=user_id).order_by('-id')
        for eachAre in are:
            newarr={
                'id':eachAre.id,
                'name':eachAre.name,
                'price':eachAre.price,
                'mrp':eachAre.mrp,
                'tagLine':eachAre.tagLing,
                'location':eachAre.location,
                'description':eachAre.description,
                'activeStatus':eachAre.activeStatus,
                'vendoractiveStatus':eachAre.vendoractiveStatus
            }
            service.append(newarr)
        return Response(service)


class viewAllServiceAdminAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        user_id=self.request.user.id
        service=[]
        are=Service.objects.all().order_by('-id')
        for eachAre in are:
            vendorDetails=User.objects.filter(id=eachAre.user_id_id).first()
            newarr={
                'id':eachAre.id,
                'name':eachAre.name,
                'price':eachAre.price,
                'mrp':eachAre.mrp,
                'tagLine':eachAre.tagLing,
                'location':eachAre.location,
                'description':eachAre.description,
                'activeStatus':eachAre.activeStatus,
                'vendoractiveStatus':eachAre.vendoractiveStatus,
                'vendor_name':vendorDetails.name,
                'vendor_email':vendorDetails.email,
                'vendor_phone':vendorDetails.phone,
                'vendor_id':vendorDetails.id,
            }
            service.append(newarr)
        return Response(service)



class addServiceAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        user_id=self.request.user.id
        inputs=request.data
        Service.objects.create(
            name=inputs['name'],
            image=inputs['image'],
            tagLing=inputs['tagLine'],
            description=inputs['description'],
            mrp=inputs['mrp'],
            price=inputs['price'],
            location=inputs['location'],
            user_id_id=user_id
        )
        newarr={
            'msg':'service add successfully',
            'status':1,

        }
        return Response(newarr)


class viewSingleServiceAdminAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get(self,request,id):
        user_id=self.request.user.id
        service=[]
        eachAre=Service.objects.filter(id=id).first()
        newarr={
            'id':eachAre.id,
            'name':eachAre.name,
            'price':eachAre.price,
            'mrp':eachAre.mrp,
            'tagLine':eachAre.tagLing,
            'location':eachAre.location,
            'description':eachAre.description,
            'activeStatus':eachAre.activeStatus,
            'vendoractiveStatus':eachAre.vendoractiveStatus,
            'img':str(eachAre.image)
        }
        return Response(newarr)




class EnquiryAPIView(ListCreateAPIView):
    serializer_class = EnquirySerializer
    queryset = Enquiry.objects.all()

    def perfrom_create(self, serializer):
        return serializer.save()


class EnquiryAPIDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = EnquirySerializer
    queryset = Enquiry.objects.all()
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()




class EnquirySubmitAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        user_id=self.request.user.id
        inputs=request.data
        Enquiry.objects.create(
            service_id_id=inputs['service_id'],
            message=inputs['message'],
            user_id_id=user_id
        )
        newarr={
            'msg':'Enquiry successfully',
            'status':1,

        }
        return Response(newarr)


class viewAllServiceUserAPIView(views.APIView):
    def get(self,request):
        service=[]
        are=Service.objects.filter(activeStatus=True,vendoractiveStatus=True).order_by('-id')
        for eachAre in are:
            newarr={
                'id':eachAre.id,
                'name':eachAre.name,
                'price':eachAre.price,
                'mrp':eachAre.mrp,
                'tagLine':eachAre.tagLing,
                'location':eachAre.location,
                'description':eachAre.description,
                'img':str(eachAre.image)
            }
            service.append(newarr)
        return Response(service)


class viewSingleServiceUserAPIView(views.APIView):
    def get(self,request,id):
        service=[]
        eachAre=Service.objects.filter(id=id).first()
        newarr={
            'id':eachAre.id,
            'name':eachAre.name,
            'price':eachAre.price,
            'mrp':eachAre.mrp,
            'tagLine':eachAre.tagLing,
            'location':eachAre.location,
            'description':eachAre.description,
            'activeStatus':eachAre.activeStatus,
            'vendoractiveStatus':eachAre.vendoractiveStatus,
            'img':str(eachAre.image)
        }
        return Response(newarr)

class getVendorEnquiryAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get(self,request):
        user_id=self.request.user.id
        enquiry=[]
        are=Enquiry.objects.all().order_by('-id')
        for eachAre in are:
            serviceDetails=Service.objects.filter(id=eachAre.service_id_id).first()
            userDetails=User.objects.filter(id=eachAre.user_id_id).first()
            if serviceDetails.user_id_id==user_id:
                newarr={
                    'id':eachAre.id,
                    'service_id':serviceDetails.id,
                    'name':serviceDetails.name,
                    'price':serviceDetails.price,
                    'mrp':serviceDetails.mrp,
                    'tagLine':serviceDetails.tagLing,
                    'location':serviceDetails.location,
                    'description':serviceDetails.description,
                    'img':str(serviceDetails.image),
                    'user_name':userDetails.name,
                    'user_email':userDetails.email,
                    'user_phone':userDetails.phone,
                    'message':eachAre.message,
                    'status':eachAre.status,

                }
                enquiry.append(newarr)
        return Response(enquiry)


class getUserEnquiryAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get(self,request):
        user_id=self.request.user.id
        enquiry=[]
        are=Enquiry.objects.filter(user_id_id=user_id).order_by('-id')
        for eachAre in are:
            serviceDetails=Service.objects.filter(id=eachAre.service_id_id).first()
            userDetails=User.objects.filter(id=eachAre.user_id_id).first()
            vendorDetails=User.objects.filter(id=serviceDetails.user_id_id).first()
            newarr={
                'id':eachAre.id,
                'service_id':serviceDetails.id,
                'name':serviceDetails.name,
                'price':serviceDetails.price,
                'mrp':serviceDetails.mrp,
                'tagLine':serviceDetails.tagLing,
                'location':serviceDetails.location,
                'description':serviceDetails.description,
                'img':str(serviceDetails.image),
                'user_name':userDetails.name,
                'user_email':userDetails.email,
                'user_phone':userDetails.phone,
                'vendor_name':vendorDetails.name,
                'vendor_email':vendorDetails.email,
                'vendor_phone':vendorDetails.phone,
                'message':eachAre.message,
                'date':eachAre.date,
                'status':eachAre.status,

            }
            enquiry.append(newarr)
        return Response(enquiry)


class getAdminEnquiryAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get(self,request):
        enquiry=[]
        are=Enquiry.objects.all().order_by('-id')
        for eachAre in are:
            serviceDetails=Service.objects.filter(id=eachAre.service_id_id).first()
            userDetails=User.objects.filter(id=eachAre.user_id_id).first()
            vendorDetails=User.objects.filter(id=serviceDetails.user_id_id).first()
            newarr={
                'id':eachAre.id,
                'service_id':serviceDetails.id,
                'name':serviceDetails.name,
                'price':serviceDetails.price,
                'mrp':serviceDetails.mrp,
                'tagLine':serviceDetails.tagLing,
                'location':serviceDetails.location,
                'description':serviceDetails.description,
                'img':str(serviceDetails.image),
                'user_name':userDetails.name,
                'user_email':userDetails.email,
                'user_phone':userDetails.phone,
                'vendor_name':vendorDetails.name,
                'vendor_email':vendorDetails.email,
                'vendor_phone':vendorDetails.phone,
                'vendor_id':vendorDetails.id,
                'message':eachAre.message,
                'status':eachAre.status,

            }
            enquiry.append(newarr)
        return Response(enquiry)