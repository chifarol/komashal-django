from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Generic "status" options
GENERIC_STATUS=[
        ("active","Active"),
        ("inactive","Cancelled")
    ]

# eligible states for delivery
class Region(models.Model):
    state = models.CharField(max_length=100, blank=False, null=False, unique=True)
    status=models.CharField(max_length=100, blank=False, default="active", choices=GENERIC_STATUS)

# eligible cities in states for delivery
class City(models.Model):
    region_id = models.ForeignKey(Region, related_name="cities", on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=100, blank=False, null=False,  unique=True)
    status=models.CharField(max_length=100, blank=False, default="active", choices=GENERIC_STATUS)


# user shipping addresses
class Address(models.Model):
    delivery_address = models.CharField(max_length=250, blank=False, null=False)
    state = models.ForeignKey(Region, related_name="addresses", on_delete=models.CASCADE, blank=False)
    city = models.ForeignKey(City, related_name="addresses", on_delete=models.CASCADE, blank=False)
    additional_info = models.CharField(max_length=250, blank=True, default="")

# company pickup station addresses
class PickupStation(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    address_id = models.ForeignKey(Address, related_name="pickup_stations", on_delete=models.CASCADE, default=1)

  

# user shipping addresses
class UserAddress(models.Model):
    ADDRESS_TYPES = [
        ('user_address', 'User Address'),
        ('pickup_address', 'Pickup Station Address'),
    ]
    user_id = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, related_name="users", on_delete=models.CASCADE, blank=False)
    first_name = models.CharField(max_length=250, blank=False, null=False, default="")
    last_name = models.CharField(max_length=250, blank=False, null=False, default="")
    phone = models.CharField(max_length=250,default="", blank=False)
    alt_phone = models.CharField(max_length=250, blank=True, default="")
    type=models.CharField(max_length=100, blank=False, default="user_address", choices=ADDRESS_TYPES)
    status=models.CharField(max_length=100, blank=False, default="active", choices=GENERIC_STATUS)
    

# promotion or discounts
class Promotion(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)
    description = models.CharField(max_length=250, blank=True, default="")
    discount_rate = models.IntegerField(default=0, validators=[ MaxValueValidator(100),  MinValueValidator(0) ])
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)

# coupons
class Coupon(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)
    description = models.CharField(max_length=250, blank=True, default="")
    discount_rate = models.IntegerField(default=0, validators=[ MaxValueValidator(100),  MinValueValidator(0) ])
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)

    token=models.CharField(max_length=100, blank=False)
    
# brands
class Brand(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.CharField(max_length=250, blank=True, default="")
    status=models.CharField(max_length=100, blank=False, default="active", choices=GENERIC_STATUS)

# Product Categories
class ProductCategory(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="child_category", null=True, blank=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.CharField(max_length=250, blank=True, default="")
    status=models.CharField(max_length=100, blank=False, default="active", choices=GENERIC_STATUS)


# Products
class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, default="")
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, related_name="products", null=True, blank=False)
    status=models.CharField(max_length=100, blank=False, default="active", choices=GENERIC_STATUS)

# Product Items
class ProductItem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="product_items", blank=False, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, default="")
    brand_id = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True,related_name="product_items", null=True)
    price = models.DecimalField(blank=False, decimal_places=2, default=0.00, max_digits=100000000)
    qty_in_stock = models.IntegerField(default=0, blank=False)
    status=models.CharField(max_length=100, blank=False, default="active", choices=GENERIC_STATUS)

# Product Images
class ProductImage(models.Model):
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

# Product Promotion
class ProductPromotion(models.Model):
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="promos")
    promotion_id=models.ForeignKey(Promotion, on_delete=models.CASCADE,related_name="products")
    status=models.CharField(max_length=100, blank=False, default="active", choices=GENERIC_STATUS)

# Product Coupon
class ProductCoupon(models.Model):
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="coupons")
    coupon_id=models.ForeignKey(Coupon, on_delete=models.CASCADE,related_name="products")
    status=models.CharField(max_length=100, blank=False, default="active", choices=GENERIC_STATUS)

# Orders
class Order(models.Model):
    ORDER_STATUS=[
        ("delivered","Delivered"),
        ("in_transit","In Transit"),
        ("pending","Pending"),
        ("cancelled","Cancelled"),
    ]
    PAYMENT_METHODS=[
        ("online","Pay Online"),
        ("on_delivery","Pay on Delivery"),
    ]
    SHIPPING_METHODS=[
        ("pickup_station","Pickup Station"),
        ("door_delivery","Door Delivery"),
    ]
    user_id= models.ForeignKey(User, on_delete=models.SET_NULL, related_name="orders", null=True)

    date= models.DateTimeField(auto_now_add=True)

    payment_method=models.CharField(max_length=100, blank=False, default="online", choices=PAYMENT_METHODS)

    shipping_method=models.CharField(max_length=100, blank=False, default="pickup_station", choices=SHIPPING_METHODS)

    address= models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name="orders")

    date= models.DateTimeField(auto_now_add=True)

    total= models.DecimalField(default=0.00, decimal_places=2, max_digits=100000000)
    
    status=models.CharField(max_length=100, blank=False, default="pending", choices=ORDER_STATUS)

# Carts
class Cart(models.Model):
    CART_STATUS = [
        ('not_checked_out','Yet to Check Out'),
        ('checked_out','Has Checked Out'),
    ]
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,related_name="carts")
    status = models.CharField(max_length=100, blank=False, default="checked_out", choices=CART_STATUS)
    

# Cart Items
class CartItem(models.Model):
    cart_id=models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="items")
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE,related_name="in_carts")

# Wishlist Items
class Wishlist(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,related_name="wishlist")
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE,related_name="in_wishlist")

# User Review 
class UserReview(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,related_name="reviews")
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE,related_name="reviews")
    rating_value=models.IntegerField(default=3, validators=[ MaxValueValidator(5),  MinValueValidator(1) ])
    comment=models.CharField(max_length=250, blank=True, default="")


