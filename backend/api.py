from .models import Region, City,  Address, UserAddress, PickupStation,Brand, ProductCategory,ProductImage, Promotion, Coupon,ProductCoupon,  ProductPromotion, Product, ProductItem,  Cart, CartItem, Order, Wishlist, UserReview, Profile

from django.contrib.auth.models import User
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from .serializers import UserSerializer, AdminUserSerializer, RegisterSerializer, RegionSerializer
from rest_framework.response import Response

from knox.models import AuthToken
from django.http import JsonResponse
from rest_framework.response import Response


# cloudinary  

import cloudinary
from pathlib import Path
import time
import os

import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent

#superadmin username
SUPERADMIN_USERNAME = env('SUPERADMIN_USERNAME')
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Profile.objects.create(user=user)
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

#make super admin user an admin
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def super_admin_user(req):
    if req.data['username'] == SUPERADMIN_USERNAME:
        try:
            req.user.is_staff=True
            req.user.save()
            admin_user=AdminUserSerializer(req.user).data
            content={'info':'super admin user created', 'admin_user':admin_user}
            return Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            content={'info':str(e), }
            return Response(content, status=status.HTTP_404_NOT_FOUND)


#make user an admin
@api_view(['POST', 'GET'])
@permission_classes((IsAdminUser,))
def admin_user(req):
    # get admin users
    if req.method == 'GET':
        try:
            admin_users = User.objects.filter(is_staff=True)
            admin_users = AdminUserSerializer(admin_users, many=True).data
            content={'info':'admin users found', 'admin_users':admin_users}
            return Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            content={'info':str(e), }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
            
    # modify user admin status
    elif req.method == 'POST':
        target_username = req.data['username']
        staff_status = req.data['is_staff']
        user_exists = User.objects.filter(username=target_username).exists()
        if not user_exists:
            content={'info':'User does not exist', }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif target_username == SUPERADMIN_USERNAME:
            content={'info':'Cannot modify super admin user status', }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.filter(username=target_username)
                user.update(is_staff=staff_status)
                user = AdminUserSerializer(user, many=True).data
                content={'info':'user staff status updated','user':user}
                return Response(content, status=status.HTTP_201_CREATED)
            except Exception as e:
                content={'info':str(e), }
                return Response(content, status=status.HTTP_501_NOT_IMPLEMENTED)

    


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def current_user(req):
    if req.method == 'GET':
        try:
            current_user = UserSerializer(req.user, many=False).data
            content={'info':'current user found', 'current_user':current_user}
            return Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            content={'info':str(e), }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
            
    # update user profile
    elif req.method == 'POST':
            try:
                Profile.objects.filter(user=req.user).update(**req.data)
                user = UserSerializer(req.user, many=False).data
                content={'info':'user status updated','user':user}
                return Response(content, status=status.HTTP_201_CREATED)
            except Exception as e:
                content={'info':str(e), }
                return Response(content, status=status.HTTP_501_NOT_IMPLEMENTED)
#HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_501_NOT_IMPLEMENTED

# regio api
@api_view(['POST','GET','PATCH','DELETE'])
@permission_classes((IsAdminUser,))
def region(req):
    # fetch region
    if req.method == 'GET':
        try:
            region_obj = Region.objects.get(id=req.GET.get('id'))
            region = RegionSerializer(region_obj).data
            content={'info':'region found', 'region':region}
            return Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            content={'info':str(e), }
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
            except Exception as e:
                content={'info':str(e), }
                return Response(content, status=status.HTTP_501_NOT_IMPLEMENTED)

    # update region
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
            except Exception as e:
                content={'info':str(e), }
                return Response(content, status=status.HTTP_501_NOT_IMPLEMENTED)
                
    # delete region
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
            except Exception as e:
                content={'info':str(e), }
                return Response(content, status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def regions(req):
    #fetch many regions
    if req.method == 'GET':
        limit = req.GET.get('limit')
        try:
            region_obj = Region.objects.all()[:limit]
            region = RegionSerializer(region_obj).data
            content={'info':'regions found', 'region':region}
            return Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            content={'info':str(e), }
            return Response(content, status=status.HTTP_404_NOT_FOUND)