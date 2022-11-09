from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, UserSerilializer
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.shortcuts import  get_object_or_404

from django.contrib.auth.models import Group, User

from rest_framework import viewsets


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
        if menuitem_count == 0:
            return Response({"message:": "no item in cart"})

        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        order_serializer = OrderSerializer(data=data)
        if (order_serializer.is_valid()):
            order = order_serializer.save()

            items = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem = OrderItem(
                    order=order,
                    menuitem_id=item['menuitem_id'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                orderitem.save()

            # Cart.objects.all().filter(user=self.request.user).delete()

            result = order_serializer.data.copy()
            result['total'] = total
            return Response(result)


class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Delivery Crew').exists() or request.user.groups.filter(name='Manager').exists():
            return super().update(request, *args, **kwargs)
        else:
            return Response('Not Ok')


@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']

    if username:
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
            return Response({"message": "user added to the manager group"}, 200)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
            return Response({"message": "user removed from the manager group"}, 200)

    return Response({"message": "error"}, 400)


class GroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Manager')
        items = UserSerilializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({"message": "user added to the manager group"}, 200)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"message": "user removed from the manager group"}, 200)

# @api_view(['GET', 'POST'])
# def orders(request):
#     if (request.method == 'GET'):
#         orders = Order.objects.all()
#         serialized_item = OrderSerializer(orders, many=True)
#         return Response(serialized_item.data)

#     if (request.method == 'POST'):
#         menuitem_count = Cart.objects.all().filter(user=request.user).count()
#         if menuitem_count == 0:
#             return Response({"message:": "no item in cart"})

#         data = request.data.copy()
#         total = get_total_price(request.user)

#         # return Response(total)
#         data['total'] = total
#         order_serializer = OrderSerializer(data=data)
#         if (order_serializer.is_valid()):
#             order = order_serializer.save()

#             items = Cart.objects.all().filter(user=request.user).all()

#             for item in items.values():
#                 orderitem = OrderItem(
#                     order=order,
#                     menuitem_id=item['menuitem_id'],
#                     price=item['price'],
#                     quantity=item['quantity'],
#                 )
#                 orderitem.save()

#             # Cart.objects.all().filter(user=self.request.user).delete()

#             result = order_serializer.data.copy()
#             result['total'] = total
#             return Response(result)

    


# def get_total_price(user):
#     total = 0
#     items = Cart.objects.all().filter(user=user).all()
#     for item in items.values():
#         total += item['price']
#     return total


# @api_view(['GET','PATCH'])
# def single_order(request, pk):
#     if (request.method == 'GET'):
#         order = get_object_or_404(Order,pk=pk)
#         serialized_item = OrderSerializer(order)
#         return Response(serialized_item.data)
#     if (request.method == 'PUT'):
#         return Response(pk)