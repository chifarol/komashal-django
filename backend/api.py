from .models import Region, City,  Address, UserAddress, PickupStation,Brand, ProductCategory,ProductImage, Promotion, Coupon,ProductCoupon,  ProductPromotion, Product, ProductItem,  Cart, CartItem, Order, Wishlist, UserReview

from django.contrib.auth.models import User
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from .serializers import UserSerializer, RegisterSerializer, RegionSerializer
from rest_framework.response import Response

from knox.models import AuthToken
from django.http import JsonResponse
from rest_framework.response import Response

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
        
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        user = serializer.validated_data['user']
        token= AuthToken.objects.create(user)[1]
        return super(LoginAPI, self).post(request, format=None)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def main_user(req):
    return JsonResponse({
        'id':req.user.id,
        'email':req.user.email,
        'username':req.user.username,
        })
#HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_501_NOT_IMPLEMENTED

# regio api
@api_view(['POST','GET','PATCH','DELETE'])
@permission_classes((IsAuthenticated,))
def region(req):
    # fetch region
    if req.method == 'GET':
        try:
            region_obj = Region.objects.get(id=req.GET.get('id'))
            region = RegionSerializer(region_obj).data
            content={'info':'region found', 'region':region}
            return Response(content, status=status.HTTP_200_OK)
        except:
            content={'info':'could not get region', }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
            
    #create region
    elif req.method == 'POST':
        new_state = req.data['state'].capitalize()
        region_exists = Region.objects.filter(state=new_state).exists()
        if region_exists:
            content={'info':'region name already exist', }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                new_region_obj = Region(state=new_state)
                new_region_obj.save()
                content={'info':'new region created','new_region':new_region_obj.state}
                return Response(content, status=status.HTTP_201_CREATED)
            except:
                content={'info':'could not create region', }
                return Response(content, status=status.HTTP_501_NOT_IMPLEMENTED)

        
    elif req.method == 'PATCH':
        target_id = req.data['id']
        new_state = req.data['new_state'].capitalize()
        region_exists = Region.objects.filter(id=target_id).exists()
        if not region_exists:
            content={'info':'region not found', }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                Region.objects.filter(id=target_id).update(state=new_state)
                content={'info':'region updated'}
                return Response(content, status=status.HTTP_201_CREATED)
            except:
                content={'info':'could not update region', }
                return Response(content, status=status.HTTP_501_NOT_IMPLEMENTED)
                
    elif req.method == 'DELETE':
        target_id = req.data['id']
        region_exists = Region.objects.filter(id=target_id).exists()
        if not region_exists:
            content={'info':'region not found', }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                Region.objects.filter(id=target_id).delete()
                content={'info':'region  deleted'}
                return Response(content, status=status.HTTP_200_OK)
            except:
                content={'info':'could not delete region'}
                return Response(content, status=status.HTTP_501_NOT_IMPLEMENTED)