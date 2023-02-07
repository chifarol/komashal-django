# Generated by Django 4.1.6 on 2023-02-07 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0004_alter_pickupstation_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='cart_id',
            new_name='cart',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='region_id',
            new_name='region',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='pickupstation',
            old_name='address_id',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='productcoupon',
            old_name='coupon_id',
            new_name='coupon',
        ),
        migrations.RenameField(
            model_name='productcoupon',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='productimage',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='productitem',
            old_name='brand_id',
            new_name='brand',
        ),
        migrations.RenameField(
            model_name='productitem',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='productpromotion',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='productpromotion',
            old_name='promotion_id',
            new_name='promotion',
        ),
        migrations.RenameField(
            model_name='useraddress',
            old_name='address_id',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='useraddress',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='userreview',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='userreview',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='wishlist',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='wishlist',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='backend.address'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]