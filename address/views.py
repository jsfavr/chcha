from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ShippingAddressSerializer, BillingAddressSerializer, DeliveryBoyPincodeSerializer, \
    DeliveryPincodeSerializer
from rest_framework import permissions, status, views
from .models import ShippingAddress, BillingAddress, DeliveryPincode, DeliveryBoyPincode
from django.core import serializers
from authentication.models import User
from rest_framework.response import Response
from product.permissions import IsOwner



# Create your views here.
class ShippingAddressAPIView(ListCreateAPIView):
    serializer_class = ShippingAddressSerializer
    queryset = ShippingAddress.objects.all()
    permissions = (permissions.IsAuthenticated,)

    def perfrom_create(self, serializer):
        return serializer.save()


class ShippingAddressDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ShippingAddressSerializer
    queryset = ShippingAddress.objects.all()
    permissions = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


# Create your views here.
class BillingAddressAPIView(ListCreateAPIView):
    serializer_class = BillingAddressSerializer
    queryset = BillingAddress.objects.all()
    permissions = (permissions.IsAuthenticated,)

    def perfrom_create(self, serializer):
        return serializer.save()


class BillingAddressDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BillingAddressSerializer
    queryset = BillingAddress.objects.all()
    permissions = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class DeliveryPincodeAPIView(ListCreateAPIView):
    serializer_class = DeliveryPincodeSerializer
    queryset = DeliveryPincode.objects.all()
    permissions = (permissions.IsAuthenticated,)

    def perfrom_create(self, serializer):
        return serializer.save()


class DeliveryPincodeDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DeliveryPincodeSerializer
    queryset = DeliveryPincode.objects.all()
    permissions = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()


class DeliveryBoyPincodeAPIView(ListCreateAPIView):
    serializer_class = DeliveryBoyPincodeSerializer
    queryset = DeliveryBoyPincode.objects.all()
    permissions = (permissions.IsAuthenticated,)

    def perfrom_create(self, serializer):
        return serializer.save()


class DeliveryBoyPincodeDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DeliveryBoyPincodeSerializer
    queryset = DeliveryBoyPincode.objects.all()
    permissions = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def perfrom_create(self, serializer):
        return serializer.save()
class DeliveryBoyPincodeDetailsView(views.APIView):
    def get(self,request,id):
        user_id = id
        deliveryboy_details = DeliveryBoyPincode.objects.filter(user_id_id=user_id)
        user_del = User.objects.filter(id=user_id)
        user_list = serializers.serialize('json',user_del)
        deliveryboy_list = serializers.serialize('json', deliveryboy_details)
        newdeliveryboy = {
            'user' : user_list,
            'delivery_boy':deliveryboy_list
        }
     
        # user_list = serializers.serialize('json', user_details)
        # return HttpResponse(user_list, content_type="application/json") 
        return Response(newdeliveryboy)  

class DeliveryBillingAddressView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        inputs = request.data
        user_id1=self.request.user.id
        #print(user_id1)
        billing = BillingAddress.objects.create(user_id_id=user_id1,pincode=inputs['pincode'],flat=inputs['flat'],address=inputs['address'],location=inputs['location'],city=inputs['city'],district=inputs['district'],state=inputs['state'])

        shipping = ShippingAddress.objects.filter(user_id_id=user_id1)
        if len(shipping)==0:
            ShippingAddress.objects.create(user_id_id=user_id1,pincode=inputs['pincode'],flat=inputs['flat'],address=inputs['address'],location=inputs['location'],city=inputs['city'],district=inputs['district'],state=inputs['state'],landmark='',name=inputs['name'],phone=inputs['phone'],optionalPhone=inputs['optionalPhone'])
        return Response({'address': 'Successfully Added'}, status=status.HTTP_200_OK) 


class FetchShippingAddressView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        inputs = request.data
        user_id1=self.request.user.id
        shipping = ShippingAddress.objects.filter(user_id_id=user_id1)
        modifiedProduct = []
        for eachProd1 in shipping:
            sta = DeliveryPincode.objects.filter(pincode=eachProd1.pincode,activeStatus=1)
            if len(sta)==0:
                status='NO'
            else:
                status='YES'

            newrel = {
                "id": eachProd1.id,
                "user_id": eachProd1.user_id_id,
                "pincode": eachProd1.pincode,
                "flat": eachProd1.flat,
                "address": eachProd1.address,
                "location": eachProd1.location,
                "landmark": eachProd1.location,
                "city": eachProd1.city,
                "district": eachProd1.district,
                "state": eachProd1.state,
                "name": eachProd1.name,
                "phone": eachProd1.phone,
                "optionalPhone": eachProd1.optionalPhone,
                "active_status":status
            }

            modifiedProduct.append(newrel)
        return Response(modifiedProduct) 
class FetchBillingAddressView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get(self,request):
        user_id1=self.request.user.id
        shipping = BillingAddress.objects.filter(user_id_id=user_id1).first()
        newrel = {
            "id": shipping.id,
            "user_id": shipping.user_id_id,
            "pincode": shipping.pincode,
            "flat": shipping.flat,
            "address": shipping.address,
            "landmark": shipping.location,
            "city": shipping.city,
            "district": shipping.district,
            "state": shipping.state,
        }
        return Response(newrel) 
class userListPincode(views.APIView):
    def get(self,request,pincode):
        userDetails = []
        deliveryboy_details = DeliveryBoyPincode.objects.filter(pincode=pincode)
        for each in deliveryboy_details:
            user = User.objects.filter(id=each.user_id_id)
            for us in user:
                newArray = {
                    "name":us.name,
                    "id":us.pk
                }
                userDetails.append(newArray)
        return Response(userDetails)


class deliveryBoyPincodeADD(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def post(self,request):
        inputs = request.data
        user_id=self.request.user.id
        deliveryboy_details = DeliveryBoyPincode.objects.filter(user_id_id=user_id,pincode=inputs['pincode']).count()
        if(deliveryboy_details==0):
            d=DeliveryBoyPincode.objects.create(user_id_id=user_id,pincode=inputs['pincode'],activeStatus=True)
            if(d):
                newArray = {
                    "status":0,
                    "message":'Pincode added successfully.'
                }
            else:
                newArray = {
                    "status":0,
                    "message":'Somethings Wrong. Please try again later.'
                }


        else:
            newArray = {
                "status":0,
                "message":'Pincode already added.'
            }
        return Response(newArray)


    
        