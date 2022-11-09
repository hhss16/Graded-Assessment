from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer
from rest_framework.response import Response

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

        def get_queryset(self):
            return Cart.objects.all().filter(user=self.request.user)

        def delete(self, *args, **kwargs):
            Cart.objects.all().filter(user=self.request.user).delete()
            return Response("ok")

class OrderView(generics.ListCreateAPIView):
        queryset = Order.objects.all()
        serializer_class = OrderSerializer
        permission_classes = [IsAuthenticated]

        def create(self, request, *args, **kwargs):
            serializer = OrderSerializer(data=request.data)
            if(serializer.is_valid()):
                order = serializer.save()
                return Response(order.id)

        

    