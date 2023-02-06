from django.contrib import admin
from .models import Region, City,  Address, UserAddress, PickupStation,Brand, ProductCategory,ProductImage, Promotion, Coupon,ProductCoupon,  ProductPromotion, Product, ProductItem,  Cart, CartItem, Order, Wishlist, UserReview

from django.contrib.auth.models import User

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id','state', 'status')
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'region_id', 'name', 'status')

@admin.register(PickupStation)
class PickupStationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address_id')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery_address', 'state', 'city')

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'address_id', 'first_name', 'last_name', 'phone', 'alt_phone')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'discount_rate', 'start_date', 'end_date')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'discount_rate', 'start_date', 'end_date', 'token')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'status')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name', 'description', 'status')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'id', 'name', 'description', 'category', 'status')

@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'name', 'description', 'brand_id', 'price', 'qty_in_stock', 'status')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id',)


@admin.register(ProductPromotion)
class ProductPromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'promotion_id', 'status')


@admin.register(ProductCoupon)
class ProductCouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'coupon_id', 'status')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'date', 'payment_method', 'shipping_method', 'address', 'date', 'total', 'status')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id','status')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart_id', 'product_id')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'product_id')

@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'product_id', 'rating_value', 'comment')


# Register your models here.
