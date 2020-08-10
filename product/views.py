from django.shortcuts import render
from django.contrib.auth.models import Group
from django.core.files import File
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from product.serializer import *
from productCategory.models import ProductCategory

from rest_framework import serializers

from product.models import  *


"""
Item_condition views
"""

"""
Item_condition views
"""


class ItemConditionsList(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """
    View the list of item_conditions, and add new ones
    """
    queryset = ConditionItems.objects.all()
    serializer_class = ItemConditionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_grp = user.groups.first()
        admin_grp = Group.objects.filter(name='Administrator').first()

        ic_title = request.data.get('title')
        ic_title_lower = ic_title.lower()

        titles = []

        if user_grp != admin_grp:
            return Response({"detail": "You are not allowed to perform such operation"}, status=403)

        if ic_title is None:
            return Response({"detail": "Bad request"}, status=400)

        item_conds = ConditionItems.objects.all()

        for item_cond in item_conds:
            titles.append(item_cond.title.lower())

        for t in titles:
            if t == ic_title_lower:
                return Response({"detail": "Product set already exists"}, status=409)

        # request.data['created_by'] = str(user.pk)
        return self.create(request, *args, **kwargs)


class ItemConditionDetails(generics.GenericAPIView,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    """
    View to deal with a particular item_condition
    """
    queryset = ConditionItems.objects.all()
    serializer_class = ItemConditionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user_grp = user.groups.first()
        admin_grp = Group.objects.filter(name='Administrator').first()

        item_condition = self.get_object()

        products = Producte.objects.filter(item_condition=item_condition)

        if len(products) > 0:
            return Response({"detail": "You are not allowed to perform such operation"}, status=403)

        if user_grp == admin_grp:
            item_condition.delete()
            return Response(None, status=204)

        return Response({"detail": "You are not allowed to perform such operation"}, status=403)


"""
product views
"""


class ProductList(generics.GenericAPIView,
              mixins.ListModelMixin,
              mixins.CreateModelMixin):
    serializer_class = ProductSerializer
    ordering = ['title']
    ordering_fields = ['title']
    queryset = Producte.objects.filter(is_deleted=False)
    search_fields = ( 'title')
    filter_fields =  ['title' ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_id = user.id
        store = Stock.objects.filter(workers=user_id).first()

        if not store or store.is_deleted:
            return Response({"detail": "Store not found"}, status=404)

        if not store.is_active:
            return Response({"detail": "Store not activated yet"}, status=403)

        title = request.data.get('title')
        image = request.data.get('image')
        description = request.data.get('description')
        price = request.data.get('price', 0)
        delivery_fee = request.data.get('delivery_fee', 0)
        quantity=request.data.get('quantity',0)
        item_condition = ConditionItems.objects.filter(id=request.data.get('item_condition')).first()
        category = ProductCategory.objects.filter(id=request.data.get('category')).first()
        brand = Brand.objects.filter(id=request.data.get('brand')).first()



        if not title or not image or not description or not item_condition or not category:

            return Response({'detail': 'Bad Request'}, status=400)

        product = Producte.objects.create(
            title=title,
            image=image,
            description=description,
            price=float(price),
            quantity=quantity ,
            delivery_fee=float(delivery_fee),
            item_condition=item_condition,
            category=category,
            brand=brand,
            stock=store
        )

        response_data = ProductSerializer(product, context={'request': request}).data
        return Response(response_data, status=201)


"""
PRODUCT DETAIL VIEWS
"""

class ProductDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Producte.objects.all()
    #permission_classes = (IsAuthenticated,)


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser or user.is_staff:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"detail": "You are not allowed to perform such action."}, status=403)






# This view list all products in a manager's or worker's store

def get_store_products(request):
    user=request.user
    user_group=user.groups.first()
    stock_manager=Group.objects.get(name='Manager')
    stock_worker=Group.objects.get(name='Worker')

    if user_group==stock_worker or user_group==stock_manager:
        store=Stock.objects.filter(workers=user).first()
        if not store:
            return Response({"detail":"store not found"})
        products=Producte.objects.filter(stock=store)
        serialized_data = ProductSerializer(products, context={'request': request}, many=True)
        return Response(serialized_data.data,status=204)
    return Response({"detail": "You are not allowed to perform such operation"}, status=403)








"""
DISCOUNTS VIEWS
"""

class DiscountList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    serializer_class = DiscountSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return DiscountOffer.objects.all()


        user_group = user.groups.first()
        if user_group.name == 'Manager':
            return DiscountOffer.objects.all()

        if user_group.name == 'Buyer':
            return DiscountOffer.objects.filter(user=user)

        return DiscountOffer.objects.none()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

"""
Product reviews
"""
class ProductReviewsList(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """
    View to list all products, and to add new ones
    """
    queryset = ProductReviewers.objects.all()
    serializer_class = ProductReviewsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_fields = '__all__'
    ordering_fields = '__all__'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        #request.data['reviewer'] = str(request.user.id)
        return self.create(request, *args, **kwargs)
