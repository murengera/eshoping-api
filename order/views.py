from django.shortcuts import render
import time
from django.contrib.auth.models import Group
from rest_framework import generics,mixins
from rest_framework.decorators import api_view, permission_classes
from  rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from product.models import Producte
from  store.models import Stock

from order.models import Order
from order.serializer import OrderSerializer

"""
order
"""




class OrderList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    serializer_class = OrderSerializer

    #permission_classes = (IsAuthenticated,)
    filter_fields = ('user', 'status', 'id', 'referance_code', 'finished_at')

    def get_queryset(self):
        queryset = Order.objects.none()
        users = self.request.user
        user_group = users.groups.last()
        buyer = Group.objects.filter(name='Buyer').first()
        store_manager = Group.objects.filter(name='Manager').first()
        store_worker = Group.objects.filter(name='Worker').first()
        admin_grp = Group.objects.filter(name='Administrator').first()

        if user_group == buyer:
            queryset = Order.objects.filter(buyer=users)

        if user_group == store_manager or user_group == store_worker:
            store = Stock.objects.filter(workers=users).first()
            queryset = Order.objects.filter(store=store)
        if user_group == admin_grp:
            queryset = Order.objects.all()

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
         return  self.create(request,*args,**kwargs)


class OrderDetails(generics.GenericAPIView,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin):
    """
    View to deal a particular order
    """
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        queryset = Order.objects.none()

        user = self.request.user
        user_group = user.groups.last()

        buyer = Group.objects.get(name='Buyer')
        store_manager = Group.objects.get(name='Manager')
        store_worker = Group.objects.get(name='Worker')

        if user_group == buyer:
            queryset = Order.objects.filter(buyer=user)

        if user_group == store_manager or user_group == store_worker:
            store = Stock.objects.filter(workers=user).first()
            queryset = Order.objects.filter(store=store)

        if user.is_staff:
            queryset = Order.objects.all()

        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.patch(request,*args,**kwargs)










""""
order view
"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_order(request):
    data = {}
    user = request.user
    orders = Order.objects.filter(buyer=user,status='NEW') | Order.objects.filter(buyer=user,status='ACTIVE')
    print(orders)
    if orders and len(orders) > 0:
        order = orders[0]
        data = OrderSerializer(order).data
        data['is_found'] = True
    else:
        data['is_found'] = False

    return Response(data, status=200)





@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def activate_order(request):
    user=request.user
    status='ACTIVE'
    if user:
        user_group=user.groups.first()
        manager = Group.objects.filter(name='Administrator').first()
        if user_group==manager:
            order= Order.objects.filter( status='NEW').first()

            print(order)
            if order:
                order.status=status
                order.save()
                return Response({"detail":"Order has been activated successfully"}, status=200)
            return  Response({"detail":"Order not found to be activated "},status=400)
        return  Response({"detail":"You are not allowed to activate ord;er "},status=403)
    return  Response({"detail":"bad request"},status=400)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def finish_order(request):
    user=request.user
    status='FINISHED'
    if user:
        user_group=user.groups.first()
        manager = Group.objects.filter(name='Administrator').first()
        if user_group==manager:
            order=Order.objects.filter(status='ACTIVE').first()

            print(order)
            if order:
                order.status=status
                order.save()
                return Response({"detail":"Order has been finished successfully"}, status=200)
            return  Response({"detail":"Order not found to be finished "},status=400)
        return  Response({"detail":"You are not allowed to finish order "},status=403)
    return  Response({"detail":"bad request"},status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFinishedOrder(request):
    user = request.user

    user_group = user.groups.first()
    if user_group.name == 'Manager' :
        start_date = request.data.get('created_at')
        end_date = request.data.get('finished_at')
        orders = Order.objects.filter(created_at__range=[start_date, end_date])
        if orders:
            response = []
            for order in orders:
                response.append(OrderSerializer(order).data)
            return Response(response,status=200)
        return Response({"detail":"Orders Not found"},status=400)
    else:
        return Response({"detail":"you are not allowed to make this Action"},status=403)

    return Response({"detail":"bad request"},status=400)











