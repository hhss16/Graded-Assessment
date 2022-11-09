from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from decimal import Decimal

from .models import Category, MenuItem, Cart, Order, OrderItem

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title', 'slug']
    

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all()
    )
    class Meta:
        model = MenuItem
        fields = ['id','title','price','category', 'featured']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset = MenuItem.objects.all()
    )

    # price = serializers.DecimalField(max_digits=5, decimal_places=2)

    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs

    class Meta:
        model = Cart
        fields =  ['user','menuitem','quantity','unit_price','price']
        extra_kwargs = {
            'price':{'read_only':True}
        }

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null = True
    )
    class Meta:
        model = Order
        fields = ['id','user','delivery_crew','status', 'date', 'total']