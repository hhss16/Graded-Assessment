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
            menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
            if menuitem_count==0:
                 return Response({"message:":"no item in cart"})

            data = request.data.copy()
            total = self.get_total_price(self.request.user)
            data['total'] = total
            order_serializer = OrderSerializer(data=data)
            if(order_serializer.is_valid()):
                order = order_serializer.save()


                items = Cart.objects.all().filter(user=self.request.user).all()
                
                for item in items.values():
                    orderitem = OrderItem(
                        order=order,
                        menuitem_id = item['menuitem_id'],
                        price = item['price'],
                        quantity = item['quantity'],
                    )
                    orderitem.save()

                # Cart.objects.all().filter(user=self.request.user).delete()

                result = order_serializer.data.copy()
                result['total'] = total;
                return Response(result)

        
        def get_total_price(self,user):
            total = 0
            items = Cart.objects.all().filter(user=user).all()
            for item in items.values():
                total += item['price']
            return total


    