from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer

class CategoriesView(generics.ListCreateAPIView):
        queryset = Category.objects.all()
        serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
        queryset = MenuItem.objects.all()
        serializer_class = MenuItemSerializer

class CartView(generics.ListCreateAPIView):
        queryset = Cart.objects.all()
        serializer_class = CartSerializer
        permission_classes = [IsAuthenticated]

class OrderView(generics.ListCreateAPIView):
        queryset = Order.objects.all()
        serializer_class = OrderSerializer
        permission_classes = [IsAuthenticated]


        

    