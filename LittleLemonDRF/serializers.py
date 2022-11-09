from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User

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

    class Meta:
        model = Cart
        fields =  ['user','menuitem','quantity','unit_price','price']