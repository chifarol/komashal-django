from rest_framework import serializers 
from django.contrib.auth.models import User

from .models import Region, City, Profile, Address, UserAddress, PickupStation,Brand, ProductCategory,ProductImage, Promotion, Coupon,ProductCoupon,  ProductPromotion, Product, ProductItem,  Cart, CartItem, Order, Wishlist, UserReview


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone', 'first_name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('state', 'status')